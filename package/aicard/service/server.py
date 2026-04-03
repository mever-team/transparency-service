import json

from aicard.card import ModelCard
from aicard.service.converters import card2format
from aicard.service.email import EmailVerification
from aicard.service.server_card_entry import ModelCardEntry
from aicard.service.assistants import Assistant, SemanticMatcher
from aicard.service.monitoring import SystemMonitor
from aicard.service import users
from aicard.service import converters
from aicard.service.logger import Logger
from aicard.utils.eval_adapter.eval_adapter import eval_adapter
from aicard.service.card_jobs import CardJobsTracker, Job
from flask import Flask, abort, redirect, request, jsonify, send_from_directory, Response, url_for
from threading import Lock
from dotenv import dotenv_values
from werkzeug.exceptions import HTTPException, Forbidden, NotFound, Unauthorized
from urllib.parse import unquote
import os.path
import traceback
import secrets
import time
import re
import pathlib

def exists(condition, message):
    # empty strings are allowed
    if condition is not None and isinstance(condition, str): return condition
    if not condition: abort(404, description=message)
    return condition

def serve(
    assistants: dict[str, Assistant],
    redirect_index: str|None = None,
    admin_username: str|None = None,
    admin_password: str|None = None,
    env: str|None = None, # retrieve missing arguments from a .env file. That can have fields USER PASS INDEX LOG (the last is the log_file)
    token_expiration_secs: int = 60*60,
    root:str|None = "db", # None or "" initializes a non-persistent database for testing
    log_file:str|None = None, # None or "" uses the console for logging
    static:str = "ui",
    domain_prefix:str="/transparency",
    third_party_realm: str|None = None,
    third_party_client: str|None = None,
    feature_extractor: SemanticMatcher|None = None,
    email_verification: EmailVerification|None = None,
    card_jobs: CardJobsTracker = CardJobsTracker(),
):
    static = os.path.abspath(static)
    if env: config = dotenv_values(env)
    else: config = dict()
    if not admin_username: admin_username = config.get("USER")
    if not admin_password: admin_password = config.get("PASS")
    if not redirect_index: redirect_index = config.get("INDEX")
    if not log_file: log_file = config.get("LOG", log_file)
    if not third_party_realm: third_party_realm = config.get("THIRD_PARTY_REALM")
    if not third_party_client: third_party_client = config.get("THIRD_PARTY_CLIENT")
    assert admin_username, f"Admin username not found in {env} USER or arguments"
    assert admin_password, f"Admin password not found in {env} PASS or arguments"
    assert redirect_index, f"Index route to redirect not found in {env} INDEX or arguments"
    import logging

    # disable flask logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    log.disabled = True

    card_cache_lock = Lock()
    card_cache: dict[int, ModelCardEntry | None] = dict()
    logger = Logger(log_file)
    monitor = SystemMonitor(logger=logger) # immediately after logger
    auth_lock = Lock()
    token2expiration = dict()
    token2user = dict()
    verification_tokens = {}
    for assistant in assistants.values():
        assistant.start(logger)
    conn = users.UserDB(logger=logger, root=root)
    app = Flask(__name__)
    empty_card = ModelCard()

    def register_third_party_token(token, user, email):
        # TODO: This strategy for occupying user names could prove frustrating. Consider some way of utilizing emails for uniqueness in the future.
        if not user: abort(401, description="Invalid username from third-party provider")
        with auth_lock:
            if token2user.get(token)==user: return
        normalized_email = (email or "").strip().lower()
        cursor = conn.conn.cursor()
        cursor.execute("SELECT username, email FROM users WHERE username = ?", (user,))
        row = cursor.fetchone()
        if not row:
            conn.insert_user("users", user, normalized_email, "", commit=True)
            db_username = user
        else:
            db_username, db_email = row
            if (db_email or "").strip().lower() != normalized_email:
                abort(403, description="Your username is occupied by another email account")
        with auth_lock: token2user[token] = db_username
    third_party_auth = users.CookieAuthenticator(third_party_realm, third_party_client, register_third_party_token, logger) if third_party_realm and third_party_client else None

    def find_card(card_id: int):
        assert isinstance(card_id, int), "Card identifier must be an integer"
        with card_cache_lock:
            card = card_cache.get(card_id, None)
            if card is None:
                # load the card from the database
                cursor = conn.conn.cursor()
                cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
                row = cursor.fetchone()
                if row:
                    col_names = [desc[0] for desc in cursor.description]
                    flattened = dict(zip(col_names, row))
                    card_creator = flattened.pop("user", "")
                    flattened.pop("id", None)
                    model_card = ModelCard()
                    model_card.data.assign_flattened(flattened)
                    card = ModelCardEntry(model_card, card_creator, conn)
                    card.card_id = card_id
                    card_cache[card_id] = card
            else:
                card.touch()
        return card

    @app.route(domain_prefix+"/<path:path>")
    def static_proxy(path):
        if domain_prefix: path = "."+domain_prefix+"/"+path
        safe_path = os.path.abspath(os.path.join(static, path)).lower()
        if (not safe_path.endswith(".html") and not safe_path.endswith(".css")
                and not safe_path.endswith(".js") and not safe_path.endswith(".png") and not safe_path.endswith(".svg")
                and not safe_path.endswith(".jpg") and not safe_path.endswith(".otf") and not safe_path.endswith(".ico")
                and not safe_path.endswith(".webp") and not safe_path.endswith(".mustache")
        ):
            logger.warn(f"WE ARE UNDER ATTACK!\n * non-web file access blocked: {safe_path!r}")
            abort(403)
        if ".env" in safe_path:
            logger.warn(f"WE ARE UNDER ATTACK!\n * .env file access blocked\n"
                        " * THIS MESSAGE REVEALS THAT ANOTHER LAYER OF PROTECTION WERE BYPASSED)")
            abort(403)
        if "env" in safe_path:
            logger.warn(f"WE ARE UNDER ATTACK!\n * file access blocked because it contains `env` in its name\n"
                        " * THIS MESSAGE REVEALS THAT TWO MORE LAYERS OF PROTECTION WERE BYPASSED)")
            abort(403)
        try:
            return send_from_directory(static, path)
        except Exception as e:
            print(e)
            logger.info(f"Path does not exist (likely an external resource): {path!r}")
            return ""

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(str(e))
        if isinstance(e, HTTPException):
            response = jsonify(error=e.description or str(e))
            response.status_code = e.code or 500
            return response
        return jsonify(error="Internal server error\nThis is not shown here for data protection, but the administrator will be notified with specifics, which may include user name and model card contents."), 500

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        if not isinstance(e, Forbidden) and not isinstance(e, NotFound) and not isinstance(e, Unauthorized): traceback.print_exc()
        logger.error(str(e))
        if isinstance(e, HTTPException):
            response = jsonify(error=e.description or str(e))
            response.status_code = e.code or 500
            return response
        return jsonify(error="Unexpected server error\nThis is not shown here for data protection, but the administrator will be notified with specifics, which may include user name and model card contents."), 500

    @app.route(domain_prefix+"/", methods=['GET'])
    def get_index():
        return redirect(redirect_index, code=307)

    @app.route("/", methods=['GET'])
    def get_index_no_prefix():
        return redirect(domain_prefix+'/'+redirect_index, code=307)

    @app.route(domain_prefix+'/users', methods=['GET'])
    @users.require_auth(token2expiration, third_party_auth)
    def admin_dashboard(token: str):
        with auth_lock: creator = token2user.get(token, "")
        if creator != admin_username:
            cursor = conn.conn.cursor()
            cursor.execute("SELECT username, email FROM users WHERE username = ?", (creator,))
            row = cursor.fetchone()
            if not row: abort(404, description="User not found")
            return jsonify({"users": [{"username": row[0], "email": row[1]}], "pending": []})
        def fetch_all_users(table_name: str):
            cursor = conn.conn.cursor()
            cursor.execute(f"SELECT username, email FROM {table_name}")
            rows = [{"username": u, "email": e} for u, e in cursor.fetchall()]
            return rows
        with monitor.lock:
            return jsonify({"users": fetch_all_users("users"), "pending": fetch_all_users("pending_users"), "resources": monitor.unsafe_status()})

    @app.route(domain_prefix+'/users/<string:username>', methods=['DELETE'])
    @users.require_admin(token2expiration)
    def delete_user(username, token: str):
        if username == admin_username: abort(403, "You are not allowed to delete the administrator account. To remove this account, first restart the service with different administrator credentials.")
        deleted = False
        for table_name in ['users', 'pending_users']:
            cur = conn.conn.execute(f"DELETE FROM {table_name} WHERE username = ?", (username,))
            if cur.rowcount: deleted = True
            conn.conn.commit()
        if not deleted: abort(404, description="User not found")
        logger.warn(username+" - deleted")
        return jsonify({"deleted": username})

    @app.route(domain_prefix + "/update_password", methods=["POST"])
    @users.require_auth(token2expiration, third_party_auth)
    def update_password(token: str):
        data = request.get_json()
        new_password = data.get("password", "")
        if not new_password: abort(400, description="Missing new password")
        with auth_lock: username = token2user.get(token)
        if not username: abort(401, description="Invalid session")
        if username == admin_username: abort(403, description="Administrator password cannot be modified via API")
        row = conn.find_user("users", username)
        if not row: abort(404, description="User not found or has been deleted")
        new_hash = users.hash_password(new_password)
        cursor = conn.conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_hash, username))
        conn.conn.commit()
        with auth_lock:
            for t, u in list(token2user.items()):
                if u == username: token2user.pop(t, None);token2expiration.pop(t, None)
            new_token = secrets.token_urlsafe(32)
            token2user[new_token] = username
            token2expiration[new_token] = time.monotonic() + token_expiration_secs
        logger.info("password updated and token rotated", user=username)
        return jsonify({"token": new_token, "expires_in": token_expiration_secs})

    @app.route(domain_prefix+'/users/<string:username>/accept', methods=['POST'])
    @users.require_admin(token2expiration)
    def promote_user(username, token: str):
        cursor = conn.conn.cursor()
        cursor.execute("SELECT username, email, password FROM pending_users WHERE username = ?",(username,))
        row = cursor.fetchone()
        if not row: abort(404, description="Pending user not found")
        cursor.execute("INSERT INTO users (username, email, password) SELECT ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?)",(row[0], row[1], row[2], row[0]))
        cursor.execute("DELETE FROM pending_users WHERE username = ?",(username,))
        conn.conn.commit()
        return jsonify({"promoted": username})

    @app.route(domain_prefix+"/register", methods=["POST"])
    def register_user():
        # we accept registration requests from the same user
        data = request.get_json()
        username = data.get("username", "")
        email = data.get("email", "")
        password = data.get("password", "") # EMPTY PASSWORD ALWAYS FAILS AT LOGING IN - USERS NEED TO SET IT UP
        username = username.replace("<", "&lt;")
        if len(username) > 64: return "Username is too long.", 400
        if not username: return "Missing username.", 400
        if not email and email_verification: return "Missing email.", 400
        if not password and not email_verification: return "Missing password. Email-based login has not been enabled for this server.", 409
        existing_user = conn.find_user('users', username)
        if existing_user:
            if existing_user[1]!=email: return "This username is associated with a different email.", 409
            if password: return "You have already registered.", 409
            if not email_verification: return "Missing password. Email-based login has not been enabled for this server.", 409 # redundant check
            # otherwise continue with normal email verification, which REQUIRES a pending user
        pending = conn.find_user('pending_users', username)
        if not pending: conn.insert_user('pending_users', username, email, password)
        elif pending[1]!=email: return "This username has already made a login request with a different email.", 409
        if email_verification:
            if password: return "This server uses email-based login. For safety, passwords can only be set after logging in.", 409
            token = secrets.token_urlsafe(32)
            with auth_lock: verification_tokens[token] = (username, time.monotonic() + token_expiration_secs)
            if not email_verification.send_email(
                email,
                "Email verification for Trustworthy AI (TrAI)",
                "Visit the link below to login with username: "+username
                +"\nThis link works only once. You can set up password-based access from your account page.\n\n"
                +url_for("verify_user", token=token, _external=True)
            ):
                return "You have already requested login with the same username and email. Wait for a minute and try again.", 409
            return jsonify({"status": "pending verification"}), 201
        return jsonify({"status": "pending approval"}), 201

    @app.route(domain_prefix + "/verify/<string:token>", methods=["GET"])
    def verify_user(token):
        with auth_lock: entry = verification_tokens.get(token)
        if not entry: abort(400, description="Verification token invalid or already used")
        username, expiry = entry
        del verification_tokens[token]
        if time.monotonic() > expiry:
            abort(400, description="Token expired")
        cursor = conn.conn.cursor()
        cursor.execute("SELECT username, email, password FROM pending_users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row: abort(404, description="Pending user not found")
        cursor.execute("INSERT INTO users (username, email, password) SELECT ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?)", (row[0], row[1], row[2], row[0]))
        cursor.execute("DELETE FROM pending_users WHERE username = ?", (username,))
        conn.conn.commit()
        with auth_lock:
            auth_token = secrets.token_urlsafe(32)
            token2expiration[auth_token] = time.monotonic() + token_expiration_secs
            token2user[auth_token] = username
            logger.info("verified and logged in", user=username)
        return redirect(domain_prefix+"/"+redirect_index+"?token="+auth_token)

    @app.route(domain_prefix+"/ping", methods=["GET"])
    def ping():
        if third_party_auth:
            auth = request.cookies.get("auth", "")
            if auth:
                auth = json.loads(unquote(auth))
                token = auth.get("token")
                payload = third_party_auth.validate_token(token)
                if not payload: return ""
                username = payload.get("username")
                email = payload.get("email")
                if not username: abort(401, description="Invalid cookie payload")
                third_party_auth.register_token(token, username, email)
                with auth_lock:
                    token2expiration[token] = time.monotonic()  # we allow always, so expire immediately
                    return jsonify({"token": token, "expires_in": token_expiration_secs, "username": token2user.get(token, "unknown")})

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "): return ""
        parts = auth.strip().split()
        if len(parts) != 2 or parts[0] != "Bearer": return ""
        with auth_lock:
            token = parts[1]
            expiry = token2expiration.get(token)
            if not expiry or time.monotonic() > expiry:
                token2expiration.pop(token, None)
                token2user.pop(token, None)
                return ""
            token2expiration[token] = time.monotonic() + token_expiration_secs
            return jsonify({"token": token, "expires_in": token_expiration_secs, "username": token2user.get(token, "unknown")})

    @app.route(domain_prefix+"/login", methods=["POST"])
    def login_user():
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "") # extra important to reject empty passwords because third-party users are assigned those
        if not username: abort(401, description="Invalid credentials - missing username")
        if not password: abort(401, description="Invalid credentials - missing password")
        with auth_lock:
            if username == admin_username and password == admin_password:
                token = secrets.token_urlsafe(32)
                token2expiration[token] = time.monotonic() + token_expiration_secs
                token2user[token] = username
                logger.warn("logged in as administrator", user=username)
                return jsonify({"token": token, "admin": True, "expires_in": token_expiration_secs})
        row = conn.find_user('users', username)
        if not row: abort(401, description=f"Invalid credentials - wrong username {username} or password")
        stored_hash = row[2]
        if not users.verify_password(password, stored_hash): abort(401, description=f"Invalid credentials - wrong username {username} or password")
        with auth_lock:
            token = secrets.token_urlsafe(32)
            token2expiration[token] = time.monotonic() + token_expiration_secs
            token2user[token] = username
        logger.info("logged in", user=username)
        return jsonify({"token": token, "admin": False, "expires_in": token_expiration_secs})

    @app.route(domain_prefix+'/cards', methods=['POST'])
    def get_cards():
        data = request.get_json() or {}
        query = data.get('query', '')
        query = re.sub(r'\s+', ' ', query).strip().lower()
        query = re.sub(r'[^a-z0-9_\-\s]', '', query)

        page = min(1,max(int(data.get('page', 1)), 1))
        page_size = min(100, max(int(data.get('page_size', 5)), 1))
        owner = data.get("user", "").strip().lower()
        owner = [owner] if owner else []
        if data.get('drafts', False):
            desc_filter_simpler = ""
            desc_filter = ""
        else:
            desc_filter_simpler = "AND desc<>''"
            desc_filter = "AND cards.desc<>''"

        def sanitize_for_fts(s: str) -> str:
            s = s.strip().lower()
            s = re.sub(r'[^a-z0-9\s]', ' ', s)
            s = re.sub(r'\s+', ' ', s)
            return s

        quality_limits = float(data.get("info", 0))/100.0 # FLOAT CAST IS MANDATORY TO AVOID INJECTION
        placeholders = ','.join(['?'] * len(owner))
        # the commented filters are VULNERABLE TO SQL INJECTION and therefore we properly create ?-based argument parsing
        type_list = data.get('type', [])
        task_list = data.get('task', [])
        if isinstance(type_list, str): type_list = [type_list]
        if isinstance(task_list, str): task_list = [task_list]
        type_filter = f"AND cards.overview__type IN ("+",".join("?" for _ in type_list)+")" if type_list else ""
        task_filter = f"AND cards.overview__task IN ("+",".join("?" for _ in task_list)+")" if task_list else ""
        safe_argument_list = list() # order and positioning matters
        if type_list: safe_argument_list.extend(type_list)
        if task_list: safe_argument_list.extend(task_list)

        owner = " ".join(owner)
        query = query.strip()

        cursor = conn.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cards")
        total = cursor.fetchone()[0]
        num_pages = (total + page_size - 1) // page_size
        offset = (page - 1) * page_size
        if len(query) >= 3 and owner:
            cursor.execute(
                f"""
                SELECT
                    cards.id,
                    cards.title,
                    cards.user,
                    cards.desc,
                    cards.quality,
                    cards.timestamp,
                    cards.overview__description,
                    cards.overview__type, 
                    cards.overview__task,
                    cards.overview__date,
                    bm25(cards_fts) AS rank
                FROM cards_fts
                JOIN cards ON cards_fts.rowid = cards.id
                WHERE cards_fts MATCH ?
                  AND LOWER(cards.user) IN ({placeholders})
                  AND cards.quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  AND bm25(cards_fts) < 50
                  {desc_filter}

                UNION ALL

                SELECT
                    cards.id,
                    cards.title,
                    cards.user,
                    cards.desc,
                    cards.quality,
                    cards.timestamp,
                    cards.overview__description,
                    cards.overview__type, 
                    cards.overview__task,
                    cards.overview__date,
                    9999 AS rank   -- fallback rank for LIKE matches
                FROM cards
                WHERE LOWER(cards.title) LIKE ?
                  AND LOWER(cards.user) IN ({placeholders})
                  AND cards.quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter}

                ORDER BY rank ASC
                LIMIT ? OFFSET ?
                """,
                (sanitize_for_fts(query), owner,*safe_argument_list, f"%{query.lower()}%", owner, *safe_argument_list, page_size, offset)
            )

        elif len(query) >= 3:
            cursor.execute(
                f"""
                SELECT
                    cards.id,
                    cards.title,
                    cards.user,
                    cards.desc,
                    cards.quality,
                    cards.timestamp,
                    cards.overview__description,
                    cards.overview__type, 
                    cards.overview__task,
                    cards.overview__date,
                    bm25(cards_fts) AS rank
                FROM cards_fts
                JOIN cards ON cards_fts.rowid = cards.id
                WHERE cards_fts MATCH ?
                  AND bm25(cards_fts) < 10
                  AND cards.quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter}

                UNION ALL

                SELECT
                    cards.id,
                    cards.title,
                    cards.user,
                    cards.desc,
                    cards.quality,
                    cards.timestamp,
                    cards.overview__description,
                    cards.overview__type, 
                    cards.overview__task,
                    cards.overview__date,
                    9999 AS rank
                FROM cards
                WHERE LOWER(cards.title) LIKE ?
                  AND cards.quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter}

                ORDER BY rank ASC
                LIMIT ? OFFSET ?
                """,
                (sanitize_for_fts(query),*safe_argument_list, f"%{query.lower()}%", *safe_argument_list, page_size, offset)
            )

        elif query and owner:
            cursor.execute(
                f"""
                SELECT id, title, user, desc, quality, timestamp, overview__description, overview__type, overview__task, overview__date
                FROM cards
                WHERE LOWER(title) LIKE ?
                  AND LOWER(user) IN ({placeholders})
                  AND quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter_simpler}
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                (f"%{query.lower()}%", owner, *safe_argument_list, page_size, offset)
            )
        elif query:
            cursor.execute(
                f"""
                SELECT id, title, user, desc, quality, timestamp, overview__description, overview__type, overview__task, overview__date
                FROM cards
                WHERE LOWER(title) LIKE ?
                  AND quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter_simpler}
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                (f"%{query.lower()}%", *safe_argument_list, page_size, offset)
            )
        elif owner:
            cursor.execute(
                f"""
                SELECT id, title, user, desc, quality, timestamp, overview__description, overview__type, overview__task, overview__date
                FROM cards
                WHERE LOWER(user) IN ({placeholders})
                  AND quality >= {quality_limits}
                  {type_filter}
                  {task_filter}
                  {desc_filter_simpler}
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                (owner, *safe_argument_list, page_size, offset)
            )
        else:
            cursor.execute(
                f"""
                SELECT id, title, user, desc, quality, timestamp, overview__description, overview__type, overview__task, overview__date
                FROM cards
                WHERE quality >= {quality_limits}
                {type_filter}
                {task_filter}
                {desc_filter_simpler}
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                (*safe_argument_list, page_size, offset)
            )
        rows = cursor.fetchall()
        added_ids = set()
        results = []
        for row in rows:
            if row[0] in added_ids: continue
            added_ids.add(row[0])
            quality = float(row[4])
            timestamp = int(row[5])
            overview = row[6]
            if "<img" in overview: overview = ""
            if len(overview)>120: overview = overview[:(120-3)]+"..."
            overview_type = row[7]
            overview_task = row[8]
            overview_date = row[9]
            results.append({"id": row[0], "name": row[1], "creator": row[2], "desc": row[3], "quality": quality, "description": overview, "type": overview_type, "task": overview_task, "date": overview_date})
        return jsonify({"results": results, "pages": num_pages, "total": total})

    @app.route(domain_prefix + '/card/<int:card_id>/ask', methods=['POST'])
    def ask_card(card_id: int):
        data = request.get_json()
        question = data.get("question", "")
        assert question, "No question provided."
        card_entry = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        with card_entry: question_id = card_entry.chat_ask(question, feature_extractor)
        return jsonify({"id": question_id,})

    @app.route(domain_prefix + '/card/<int:card_id>/ask/<int:question_id>', methods=['POST'])
    def reply_card(card_id: int, question_id: int):
        card_entry = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        completing = card_entry.check_completion()
        if completing: return jsonify({"id": question_id, "answer": "...", "isfinal": False})
        with card_entry: isdone, answer = card_entry.chat_reply(question_id)
        return jsonify({"id": question_id, "answer": answer, "isfinal": isdone})

    @app.route(domain_prefix+'/card/<int:card_id>/clone', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def clone_card(card_id, token: str):
        parent_id = card_id
        with auth_lock: creator = token2user.get(token, "")
        card = ModelCardEntry(ModelCard(), creator, conn)
        parent_card = find_card(card_id)
        with exists(parent_card, "Model card does not exist or has been deleted.") as src_card:
            try: card.card.data.assign(src_card.data)
            except AssertionError as e:
                logger.warn("Assertion error: " + str(e))
                abort(500, description=str(e))
            except Exception as e:
                logger.warn("Exception: " + str(e))
                abort(500, description=str(e))
        flattened = card.card.data.flatten()
        columns = list(flattened.keys())
        cursor = conn.conn.cursor()
        cursor.execute(
            f'''INSERT INTO cards (user, desc, {','.join(columns)}) VALUES (?,?, {",".join(["?"] * len(columns))})''',
            [creator, ""] + [flattened[key] for key in columns])
        conn.conn.commit()
        card_id = cursor.lastrowid
        card.card_id = card_id
        conn.create_card_relation(parent_id=parent_id, child_id=card_id, message="")
        #conn.create_card_relation(parent_id=card_id, child_id=parent_id, message="Original")
        parent_card.commit_card(edit_message=None)
        card.card.overview.version = ""
        card.commit_card(edit_message="Clone")
        with card_cache_lock: card_cache[card_id] = card
        logger.info("cloned a card", user=creator)
        return jsonify(card_id), 201

    @app.route(domain_prefix+'/assistants', methods=['GET'])
    @users.require_auth(token2expiration, third_party_auth)
    def get_assistants(token: str):
        return jsonify([{"name": key, "desc": value.description} for key, value in assistants.items()])

    @app.route(domain_prefix+'/card/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        found = find_card(card_id)
        with exists(found, "Model card does not exist or has been deleted.") as card:
            return jsonify(converters.dict2dynamic(card.data, {"title"})
                           |{"description": card.summary(), "quality": card.quality(), "history": found.history(), "creator": found.creator})

    @app.route(domain_prefix+'/card/<int:card_id>/locked', methods=['GET'])
    def get_card_locked_status(card_id):
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        return jsonify(card.check_completion())

    @app.route(domain_prefix+'/card/<int:card_id>/title', methods=['GET'])
    def get_card_title(card_id):
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            return jsonify(card.title)

    @app.route(domain_prefix+'/card/<int:card_id>/title', methods=['PUT'])
    @users.require_auth(token2expiration, third_party_auth)
    def set_card_title(card_id, token: str):
        with auth_lock: creator = token2user.get(token, None)
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            if creator != card.creator: abort(403, "Only the card's creator can edit it.")
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card titles.")
            card.data['title'].set(json_data)
            return jsonify(card.data['title'])

    @app.route(domain_prefix+'/card/fields', methods=['GET'])
    def get_card_fields():
        return jsonify([key for key, value in empty_card.data.items() if isinstance(value, dict)])

    @app.route(domain_prefix+'/card/fields/<string:field_name>', methods=['GET'])
    def get_card_field_names(field_name):
        fields = empty_card.data
        field = exists(fields.get(field_name, None), f"Field '{field_name}' does not exist.")
        exists(isinstance(field, dict), f"Field '{field_name}' does not have data entries.")
        return jsonify(list(field.keys()))

    @app.route(domain_prefix+'/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['GET'])
    def get_card_field(card_id, field_name, data_name):
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            return jsonify(data)

    @app.route(domain_prefix+'/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['PUT'])
    @users.require_auth(token2expiration, third_party_auth)
    def set_card_field(card_id, field_name, data_name, token: str):
        with auth_lock: creator = token2user.get(token, None)
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            if creator != card.creator: abort(403, "Only the card's creator can edit it.")
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card fields.")
            data.set(json_data)
            return jsonify(data.get())  # do not return json_data directly, as setting the value may format it

    @app.route(domain_prefix+'/card/<int:card_id>', methods=['DELETE'])
    @users.require_auth(token2expiration, third_party_auth)
    def delete_card(card_id, token: str):
        with auth_lock: creator = token2user.get(token, None)
        card_entry = find_card(card_id)
        if creator != card_entry.creator: abort(403, "Only the card's creator can delete it.")
        with exists(card_entry, "Model card does not exist or has been deleted.") as card:
            cursor = conn.conn.cursor()
            cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
            conn.conn.commit()
            with card_cache_lock: del card_cache[card_id]
            logger.info("deleted a card", user=creator)
            return '', 204

    @app.route(domain_prefix+'/card/<int:card_id>', methods=['PUT'])
    @users.require_auth(token2expiration, third_party_auth)
    def update_card(card_id, token: str):
        card_entry = find_card(card_id)
        with auth_lock: creator = token2user.get(token, None)
        if creator != card_entry.creator: abort(403, "Only the card's creator can edit it.")
        json_data = request.get_json()
        with exists(card_entry, "Model card does not exist or has been deleted.") as card:
            try:
                assignable = converters.dynamic2dict(json_data, {"title"})
                card.data.assign(assignable)
                card.data.validate_integrity()
                card_entry.commit_card()
            except AssertionError as e: abort(404, "Wrong data: "+str(e))
            except Exception as e: abort(404, "Wrong data: "+str(e))
            logger.info("updated a card", user=creator)
            return jsonify(converters.dict2dynamic(card.data, {"title"})
                           |{"description": card.summary(), "quality": card.quality(), "history": card_entry.history(), "creator": card_entry.creator})

    @app.route(domain_prefix+'/card', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def create_card(token: str):
        json_data = request.get_json()
        with auth_lock: creator = token2user.get(token, "")
        card = ModelCardEntry(ModelCard(), creator, conn)
        if json_data:
            try: card.card.data.assign(converters.dynamic2dict(json_data, {"title"}))
            except AssertionError as e:
                logger.warn("Assertion error: "+str(e))
                abort(500, description=str(e))
            except Exception as e:
                logger.warn("Exception: "+str(e))
                abort(500, description=str(e))
        flattened = card.card.data.flatten()
        columns = list(flattened.keys())
        cursor = conn.conn.cursor()
        cursor.execute(f'''INSERT INTO cards (user, desc, {','.join(columns)}) VALUES (?,?, {",".join(["?"] * len(columns))})''',
                       [creator, ""] + [flattened[key] for key in columns])
        conn.conn.commit()
        card_id = cursor.lastrowid
        card.card_id = card_id
        with card_cache_lock:
            card_cache[card_id] = card
        logger.info("created a card", user=creator)
        return jsonify(card_id), 201

    @app.route(domain_prefix+'/assistant/<string:assistant_type>/complete/<int:card_id>', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def autocomplete_card(card_id: int, assistant_type: str, token: str):
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        with auth_lock: creator = token2user.get(token, None)
        if creator != card.creator: abort(403, "Only the card's creator can import information.")
        if 'file' in request.files:
            uploaded_file = request.files['file']
            exists(uploaded_file.filename != "", "Empty file uploaded")
            ext = pathlib.Path(uploaded_file.filename).suffix
            file_bytes = uploaded_file.read()
            json_data = {"data_type": ext, "bytes": file_bytes}
        else:
            json_data = {"data_type": "url", "url": request.get_json()}
            exists(isinstance(json_data['url'], str), "Import requires a url string")
        status = card.autocomplete(json_data, assistant, logger)
        logger.info(f"requested card {card_id} imported from {assistant_type}", user=creator)
        return jsonify(status)

    @app.route(domain_prefix+'/assistant/<string:assistant_type>/refine/<int:card_id>', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def autorefine_card(card_id: int, assistant_type: str, token: str):
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        with auth_lock: creator = token2user.get(token, None)
        if creator!=card.creator: abort(403, "Only the card's creator can refine it in-place.")
        status = card.autorefine(assistant, logger, card_jobs)
        logger.info(f"requested card {card_id} refinement from {assistant_type}", user=creator)
        return jsonify(status)
    
    @app.route(domain_prefix+'/assistant/<string:assistant_type>/refinefield/<int:card_id>', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def autorefine_field(card_id: int, assistant_type: str, token: str):
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        with auth_lock: creator = token2user.get(token, None)
        if creator!=card.creator: abort(403, "Only the card's creator can refine it in-place.")
        data = request.get_json()
        text = data.get('value', '')
        refined_stream = assistant.refine_field(text, logger)
        logger.info(f"requested field card {card_id} refinement from {assistant_type}", user=creator)
        return Response(refined_stream, content_type="application/x-ndjson")
    
    @app.route(domain_prefix+'/job/<int:card_id>', methods=['GET'])
    @users.require_auth(token2expiration, third_party_auth)
    def card_job(card_id: int, token: str):
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        with auth_lock: creator = token2user.get(token, None)
        if creator!=card.creator: abort(403, "Only the card's creator can see its status.")
        status = card_jobs.get(card_id)
        if status:
            return jsonify(status.to_dict())
        else:
            return jsonify({})

    @app.route(domain_prefix+"/card/<int:card_id>/download/<string:fformat>", methods=["GET"])
    def download_card(card_id, fformat):
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            content, mimetype, filename = card2format(card, fformat)
        return Response(content, mimetype=mimetype, headers={"Content-Disposition": f"attachment; filename={filename}"})

    @app.route(domain_prefix+'/eval_adapter/<int:card_id>', methods=['POST'])
    @users.require_auth(token2expiration, third_party_auth)
    def eval_adapter_endpoint(card_id, token: str):
        card_entry = find_card(card_id)
        with auth_lock: creator = token2user.get(token, None)
        if creator != card_entry.creator: abort(403, "Only the card's creator can edit it.")
        
        data = request.get_json()
        if not data:
            return abort(400, "Empty JSON")
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            try:
                html_formated_data = eval_adapter(data)
                card.data.performance.metrics += html_formated_data
                card.data.validate_integrity()
                card_entry.commit_card()
            except AssertionError as e: abort(404, "AssertionError: "+str(e))
            except Exception as e: abort(404, "Exception: "+str(e))
            logger.info("updated a card with eval data", user=creator)
            return jsonify(converters.dict2dynamic(card.data, {"title"})
                |{"description": card.summary(), "quality": card.quality(), "history": card_entry.history(), "creator": card_entry.creator})

    @app.route(domain_prefix+"/options/<string:section>/<string:field>", methods=["GET"])
    def get_options(section, field):
        try:
            return jsonify(ModelCard().data[section][field].options())
        except Exception as e:
            logger.error("No options for " + section + " " + field)
            abort(400, "No options for " + section + " " + field)

    def gc():
        while True:
            now = time.monotonic()
            one_hour = 3600
            to_delete = []
            with card_cache_lock:
                for card_id, entry in list(card_cache.items()):
                    if entry is None:
                        to_delete.append(card_id)
                        continue
                    with entry.lock:
                        if not entry._is_completing and now-entry.last_accessed>one_hour:
                            to_delete.append(card_id)
                for card_id in to_delete: card_cache.pop(card_id, None)
            time.sleep(600)  # run every 10 minutes

    logger.ok("Server is ready: http://127.0.0.1:5000"+domain_prefix)
    return app, gc, monitor
