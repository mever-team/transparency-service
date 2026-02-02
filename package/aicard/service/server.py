import os.path

from aicard.card import ModelCard
from aicard.card.model_card import truncate
from aicard.service.assistants import Assistant
from aicard.service import users
from aicard.service import converters
from aicard.service.logger import Logger
from flask import Flask, abort, redirect, request, jsonify, send_from_directory, Response
from flasgger import Swagger
from threading import Lock, Thread
from dotenv import dotenv_values
from werkzeug.exceptions import HTTPException, Forbidden, NotFound
from io import BytesIO
import traceback
import re
import json
import time
import secrets
import datetime
import io

def create_progress_bar(quality: float) -> str:
    quality = max(0.0, min(1.0, quality))
    stars = ""
    total_stars = 5
    rating = quality * total_stars
    for i in range(total_stars):
        if rating >= i + 1: stars += "★"
        elif rating > i: stars += "⯪"
        else: stars += "☆"
    return f"""<span style="color:gold; font-size:14px; letter-spacing:1px;">{stars}</span>"""

def exists(condition, message):
    # empty strings are allowed
    if condition is not None and isinstance(condition, str): return condition
    if not condition: abort(404, description=message)
    return condition

class ModelCardEntry:
    def __init__(self, card: ModelCard, creator: str, conn):
        self.card = card
        self.creator = creator
        self.preview = card.to_html_card()
        self.lock = Lock()
        self._is_completing: bool = False
        self._completion_status: list[str]|None = None
        self._completion_start = 0
        self.__thread = None
        self.conn = conn
        self.card_id = None
        self.last_accessed = time.time()

    def history(self, k: int=5):
        if self.card_id is None or k <= 0:
            return []

        cursor = self.conn.conn.cursor()
        visited = {self.card_id}
        frontier = {self.card_id}
        edges = set()
        for _ in range(k):
            if not frontier: break
            next_frontier = set()
            placeholders = ",".join("?" * len(frontier))
            cursor.execute(
                f"""
                SELECT parent_id, child_id, message
                FROM card_children
                WHERE parent_id IN ({placeholders}) OR child_id IN ({placeholders})
                """,
                tuple(frontier) * 2
            )
            for u, v, msg in cursor.fetchall():
                edges.add((u, v, msg or ""))
                if u not in visited:
                    visited.add(u)
                    next_frontier.add(u)
                if v not in visited:
                    visited.add(v)
                    next_frontier.add(v)
            frontier = next_frontier
        return list(edges)

    def touch(self):
        self.last_accessed = time.time()

    def commit_card(self, on_thread: bool = False, edit_message: str|None = "Edited"):
        flattened = self.card.data.flatten()
        assert flattened, "Cannot commit an empty model card."
        assert self.card_id is not None, "Internal error: card_id has not been set for a cached card"
        
        def strip_html_tags(text: str) -> str:
            return re.sub(r'<[^>]*>', '', text)
        if self.card.overview.name:
            self.card.title = truncate(strip_html_tags(self.card.overview.name), 30)
        quality = self.card.quality()
        summary = self.card.summary()
        if summary: desc = summary#create_progress_bar(quality)+" for "+summary
        else: desc = ""

        if edit_message:
            if edit_message == "Edited" and summary: edit_message = summary
            else: edit_message = edit_message+" " + summary
            #if desc: desc += f" [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}]"

        timestamp = int(time.time())
        columns = list(flattened.keys())
        values = [flattened[key] for key in columns]+[desc, self.card.title, quality, timestamp]
        columns += ["desc", "title", "quality", "timestamp"]  # do this after values uses columns, because its a db, not card field
        query = f'''
            UPDATE cards
            SET {", ".join(f'"{col}" = ?' for col in columns)}
            WHERE id = ?
        '''
        if on_thread:
            assert self.conn.db_path, "Database is stored on memory and cannot follow the independent thread connection model (this may be fine in testing)"
            import sqlite3
            # Open a short-lived connection just for this update
            # adjust db_path to wherever your database file lives.
            # It's fine to do this because on_thread=True is
            # reserved for agents where some ms of system operations
            # at worst are nothing in comparison.
            with sqlite3.connect(self.conn.db_path) as tmp_conn:
                if edit_message:
                    cursor = tmp_conn.execute(
                        "SELECT 1 FROM card_children WHERE parent_id = ? AND child_id = ?",
                        (self.card_id, self.card_id)
                    )
                    exists = cursor.fetchone() is not None
                    if exists:
                        tmp_conn.execute(
                            "UPDATE card_children SET message = ? WHERE parent_id = ? AND child_id = ?",
                            (edit_message, self.card_id, self.card_id)
                        )
                    else:
                        tmp_conn.execute(
                            "INSERT INTO card_children (parent_id, child_id, message) VALUES (?, ?, ?)",
                            (self.card_id, self.card_id, edit_message)
                        )
                    tmp_conn.commit()
                tmp_conn.execute(query, values + [self.card_id])
                tmp_conn.commit()
        else:
            if edit_message: self.conn.create_card_relation(parent_id=self.card_id, child_id=self.card_id, message=edit_message)
            with self.conn.conn:
                cursor = self.conn.conn.cursor()
                cursor.execute(query, values + [self.card_id])

    def start_completion(self):
        self.lock.acquire()
        if self._is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is already working on the model card")
        self._is_completing = True
        self._completion_status = ["An AI assistant is working on the model card"]
        self._completion_start = time.time()
        self.lock.release()

    def check_completion(self):
        ret = "An AI assistant is working on the model card"  # failsafe is to complain
        with self.lock:
            if not self._is_completing: ret = ""
            else: ret = "<br>".join(self._completion_status)+" ("+str(int(time.time() - self._completion_start))+" sec)"
        return ret

    def end_completion(self):
        with self.lock:
            self._is_completing = False
            self._completion_status = None
            self._completion_start = time.time()

    def __enter__(self):
        self.lock.acquire()
        if self._is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is working on the model card")
        return self.card

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    def __autocomplete(self, data: dict, assistant: Assistant, logger: Logger):
        try:
            assistant.complete(self.card, data, logger, self._completion_status)
            self.commit_card(on_thread=True, edit_message=assistant.alias+" import") # on_thread=True because we are on a heavyweight path either way
            if data['data_type'] == 'pdf' and os.path.exists(data['path']):
                os.remove(data['path'])
            logger.info(f"ended card {self.card_id} import", user=assistant.alias)
        except Exception as e:
            if data['data_type'] == 'pdf' and os.path.exists(data['path']):
                os.remove(data['path'])
            if not isinstance(e, Forbidden) and not isinstance(e, NotFound): traceback.print_exc()
            logger.error(f"aborted card{self.card_id} import with error {e}", user=assistant.alias)
        self.end_completion()

    def __autorefine(self, assistant: Assistant, logger: Logger):
        try:
            assistant.refine(self.card, logger, self._completion_status)
            self.commit_card(on_thread=True, edit_message=assistant.alias+" refinement") # on_thread=True because we are on a heavyweight path either way
            logger.info(f"ended card {self.card_id} refinement", user=assistant.alias)
        except Exception as e:
            if not isinstance(e, Forbidden) and not isinstance(e, NotFound): traceback.print_exc()
            logger.error(f"aborted card{self.card_id} refinement with error {e}", user=assistant.alias)
        self.end_completion()

    def autocomplete(self, data: dict, assistant: Assistant, logger: Logger):
        self.start_completion()
        self.__thread = Thread(target=self.__autocomplete, args=(data,assistant,logger))
        self.__thread.start()
        return "Autocompletion request was submitted successfully. Please wait while the assistant runs."

    def autorefine(self, assistant: Assistant, logger: Logger):
        self.start_completion()
        self.__thread = Thread(target=self.__autorefine, args=(assistant,logger))
        self.__thread.start()
        return "Refinement request was submitted successfully. Please wait while the assistant runs."

    def get_status(self):
        if self.check_completion(): return {"status": "locked", "message": "AI assistant is working on the model card"}
        return {"status": "editable", "message": "You can edit the model card"}

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
    domain_prefix:str="/transparency"
):
    static = os.path.abspath(static)
    if env: config = dotenv_values(env)
    else: config = dict()
    if not admin_username: admin_username = config.get("USER")
    if not admin_password: admin_password = config.get("PASS")
    if not redirect_index: redirect_index = config.get("INDEX")
    if not log_file: log_file = config.get("LOG", log_file)
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
    token2expiration = dict()
    token2user = dict()
    for assistant in assistants.values():
        assistant.start(logger)
    conn = users.UserDB(logger=logger, root=root)
    app = Flask(__name__)
    empty_card = ModelCard()
    swagger = Swagger(app, template = {
        "swagger": "2.0",
        "info": {"title": "ModelCard",
            "description": "API docs",
            "version": "0.0.4"
        }
    })

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
        if domain_prefix:
            path = "."+domain_prefix+"/"+path
        safe_path = os.path.abspath(os.path.join(static, path)).lower()
        if (not safe_path.endswith(".html") and not safe_path.endswith(".css")
                and not safe_path.endswith(".js") and not safe_path.endswith(".png") and not safe_path.endswith(".svg")
                and not safe_path.endswith(".jpg") and not safe_path.endswith(".otf") and not safe_path.endswith(".ico")
                and not safe_path.endswith(".webp")
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
        if not isinstance(e, Forbidden) and not isinstance(e, NotFound): traceback.print_exc()
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
    @users.require_admin(token2expiration)
    def admin_dashboard(token: str):
        """
        Retrieves all active and pending users.
        Requires a valid admin bearer token in the Authorization header.
        ---
        tags:
          - Admin
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for admin authentication (e.g., "Bearer <token>")
        responses:
          200:
            description: Lists of all users and pending registrations.
            schema:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
                    properties:
                      username:
                        type: string
                      email:
                        type: string
                pending:
                  type: array
                  items:
                    type: object
                    properties:
                      username:
                        type: string
                      email:
                        type: string
          401:
            description: Unauthorized — missing token or invalid token format.
          403:
            description: Unauthorized — token expired or not valid.
        """
        def fetch_all_users(table_name: str):
            cursor = conn.conn.cursor()
            cursor.execute(f"SELECT username, email FROM {table_name}")
            rows = [{"username": u, "email": e} for u, e in cursor.fetchall()]
            return rows

        return jsonify({
            "users": fetch_all_users("users"),
            "pending": fetch_all_users("pending_users")
        })

    @app.route(domain_prefix+'/users/<string:username>', methods=['DELETE'])
    @users.require_admin(token2expiration)
    def delete_user(username, token: str):
        """
        Deletes a user or pending user by username.
        Requires a valid admin bearer token in the Authorization header.
        ---
        tags:
          - Admin
        parameters:
          - name: username
            in: path
            type: string
            required: true
            description: The username to delete.
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for admin authentication (e.g., "Bearer <token>")
        responses:
          200:
            description: Successfully deleted the user.
            schema:
              type: object
              properties:
                deleted:
                  type: string
                  description: The username that was deleted.
          401:
            description: Unauthorized — missing or invalid token.
          403:
            description: Token expired or not valid for admin access.
          404:
            description: User not found.
        """
        deleted = False
        for table_name in ['users', 'pending_users']:
            cur = conn.conn.execute(f"DELETE FROM {table_name} WHERE username = ?", (username,))
            if cur.rowcount: deleted = True
            conn.conn.commit()
        if not deleted: abort(404, description="User not found")
        logger.warn(username+" - deleted")
        return jsonify({"deleted": username})

    @app.route(domain_prefix+'/users/<string:username>/accept', methods=['POST'])
    @users.require_admin(token2expiration)
    def promote_user(username, token: str):
        """
        Promotes a pending user to an active user.
        Requires a valid admin bearer token in the Authorization header.
        ---
        tags:
          - Admin
        parameters:
          - name: username
            in: path
            type: string
            required: true
            description: The username to promote.
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for admin authentication (e.g., "Bearer <token>")
        responses:
          200:
            description: User was successfully promoted.
            schema:
              type: object
              properties:
                promoted:
                  type: string
                  description: The username that was promoted.
          401:
            description: Unauthorized — missing or invalid token.
          403:
            description: Token expired or not valid for admin access.
          404:
            description: Pending user not found.
        """
        cursor = conn.conn.cursor()
        cursor.execute("SELECT username, email, password FROM pending_users WHERE username = ?",(username,))
        row = cursor.fetchone()
        if not row: abort(404, description="Pending user not found")
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",(row[0], row[1], row[2]))
        cursor.execute("DELETE FROM pending_users WHERE username = ?",(username,))
        conn.conn.commit()
        return jsonify({"promoted": username})

    @app.route(domain_prefix+"/register", methods=["POST"])
    def register_user():
        """
        Registers a new user into the pending approval list.
        Administrator acceptance is required for them to log in.
        ---
        tags:
          - Auth
        parameters:
          - name: body
            in: body
            required: true
            description: JSON object with username, email, and password.
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: Successfully registered. Pending admin approval.
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "pending approval"
          400:
            description: Missing required fields (username, email, or password).
          409:
            description: User already exists in active or pending list.
        """
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not username or not email or not password: return "Missing fields among username, email, or password", 400# abort(400, description="Missing fields among username, email, or password")
        if conn.find_user('users', username) or conn.find_user('pending_users', username): return "User already exists", 409 #abort(409, description="User already exists")
        conn.insert_user('pending_users', username, email, password)
        return jsonify({"status": "pending approval"}), 201

    @app.route(domain_prefix+"/ping", methods=["GET"])
    def ping():
        """
        Checks if the bearer token is valid.
        If valid, echoes it back and refreshes its expiration.
        Otherwise returns an empty string.
        ---
        tags:
          - Auth
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token to check validity.
        responses:
          200:
            description: Token is valid; echoed back with renewed expiration.
            schema:
              type: object
              properties:
                token:
                  type: string
                expires_in:
                  type: integer
          200:
            description: Empty string if invalid or expired.
        """
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return ""

        parts = auth.strip().split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return ""

        token = parts[1]
        expiry = token2expiration.get(token)
        if not expiry or time.time() > expiry:
            # Clean up expired entries
            token2expiration.pop(token, None)
            token2user.pop(token, None)
            return ""

        # Valid token: refresh expiration
        token2expiration[token] = time.time() + token_expiration_secs
        return jsonify({
            "token": token,
            "expires_in": token_expiration_secs
        })


    @app.route(domain_prefix+"/login", methods=["POST"])
    def login_user():
        """
        Logs in a user or the admin and returns an expiring bearer token.
        ---
        tags:
          - Auth
        parameters:
          - name: body
            in: body
            required: true
            description: JSON object with username and password.
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Login successful; bearer token issued.
            schema:
              type: object
              properties:
                token:
                  type: string
                  description: Bearer token to be used in Authorization header.
                admin:
                  type: boolean
                  description: Whether the logged-in user is an admin.
                expires_in:
                  type: integer
                  description: Token expiration time in seconds.
          401:
            description: Invalid credentials.
        """
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        if username == admin_username and password == admin_password:
            token = secrets.token_urlsafe(32)
            token2expiration[token] = time.time() + token_expiration_secs
            token2user[token] = username
            logger.warn("logged in as administrator", user=username)
            return jsonify({"token": token, "admin": True, "expires_in": token_expiration_secs})
        row = conn.find_user('users', username)
        if not row: abort(401, description="Invalid credentials")
        stored_hash = row[2]
        if not users.verify_password(password, stored_hash): abort(401, description="Invalid credentials")
        token = secrets.token_urlsafe(32)
        token2expiration[token] = time.time() + token_expiration_secs
        token2user[token] = username
        logger.info("logged in", user=username)
        return jsonify({"token": token, "admin": False, "expires_in": token_expiration_secs})

    @app.route(domain_prefix+'/cards', methods=['POST'])
    def get_cards():
        """
        Retrieves a list of model cards from the database while filtering for a search query and performing pagination.
        The results contain both card id, title, and descriptions, and the total number of pages
        for the particular pagination limit. If no query is provided, all cards will be considered.
        If no page size is provided, or if non-positive, 10 is assumed. If no page is provided,
        or if it's non-positive, 1 (the first page) is assumed.
        ---
        tags:
          - UI
        parameters:
          - name: query
            in: body
            type: string
            required: false
            description: Case-insensitive filter on card titles.
            example: "my card"
          - name: creator
            in: body
            type: string
            required: false
            description: Case-sensitive filter on card creator names.
            example: "admin"
          - name: page
            in: body
            type: integer
            required: false
            default: 1
            description: Page number, starting from 1.
          - name: page_size
            in: body
            type: integer
            required: false
            default: 10
            description: Number of results per page.
        responses:
          200:
            description: A paginated list of card summaries.
            schema:
              type: object
              properties:
                results:
                  type: array
                  description: List of card summaries.
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: Card identifier.
                      name:
                        type: string
                        description: Card title.
                      creator:
                        type: string
                        description: The creator's username.
                      desc:
                        type: string
                        description: Card description (e.g., completion percentage).
                      overview:
                        type: string
                        description: Card overview (either empty or a long description)
                pages:
                  type: integer
                  description: Total number of result pages.
        """
        data = request.get_json() or {}
        query = data.get('query', '').strip().lower()
        type_list = data.get('type', '')
        task_list = data.get('task', '')
        parts = query.split()

        page = max(int(data.get('page', 1)), 1)
        page_size = max(int(data.get('page_size', 5)), 1)
        owner = data.get("creator", "").strip().lower()
        owner = [owner] if owner else []
        desc_filter_simpler = "AND desc<>''"
        desc_filter = "AND cards.desc<>''"
        import re
        def sanitize_for_fts(s: str) -> str:
            s = s.strip().lower()
            s = re.sub(r'[^a-z0-9\s]', ' ', s)
            s = re.sub(r'\s+', ' ', s)
            return s

        # apply filters
        i = 0
        quality_limits = float(0)
        new_parts = []
        while i<len(parts):
            filter = parts[i]
            if filter=="--drafts":
                desc_filter_simpler = ""
                desc_filter = ""
            elif filter=="--by" and i<len(parts)-1:
                i += 1
                owner.append(parts[i])
            elif filter=="--info" and i<len(parts)-1:
                i += 1
                value = parts[i]
                try:
                    quality_limits = float(value)/100-0.00001
                except Exception:
                    pass
            # elif filter=="--top" and i<len(parts)-1:
            #     i += 1
            #     try:
            #         page_size = int(parts[i])
            #     except: pass
            #     if page_size<=1: page_size = 1
            #     if page_size>=50: page_size = 50
            elif filter == "--more":
                page_size = 20
            else:
                new_parts.append(filter)
            i += 1
        placeholders = ','.join(['?'] * len(owner))
        type_filter = f"AND cards.overview__type IN ('{'\',\''.join(type_list)}')" if type_list else ""
        task_filter = f"AND cards.overview__task IN ('{'\',\''.join(task_list)}')" if task_list else ""
        owner = " ".join(owner)
        query = " ".join(new_parts)
        query = query.strip()

        cursor = conn.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cards")
        total = cursor.fetchone()[0]
        num_pages = (total + page_size - 1) // page_size
        offset = (page - 1) * page_size
        if len(query) >= 3 and owner:
            placeholders = ",".join(["?"] * len(owner))
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
                (sanitize_for_fts(query), *owner, f"%{query.lower()}%", *owner, page_size, offset)
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
                (sanitize_for_fts(query), f"%{query.lower()}%", page_size, offset)
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
                (f"%{query.lower()}%", owner, page_size, offset)
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
                (f"%{query.lower()}%", page_size, offset)
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
                (owner, page_size, offset)
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
                (page_size, offset)
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
            # if len(overview)>120: overview = overview[:(120-3)]+"..."
            overview_type = row[7]
            overview_task = row[8]
            overview_date = row[9]
            results.append({"id": row[0], "name": row[1], "creator": row[2], "desc": row[3], "quality": quality, "description": overview, "type": overview_type, "task": overview_task, "date": overview_date})
        return jsonify({"results": results, "pages": num_pages, "total": total})

    @app.route(domain_prefix+'/card/<int:card_id>/clone', methods=['POST'])
    @users.require_auth(token2expiration)
    def clone_card(card_id, token: str):
        """
        Clones an existing model card into a new one owned by the current user.
        The new card will have the same content but a new ID and creator. Its version
        will also be cleared out to not make it searchable yet.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The ID of the card to clone.
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            201:
                description: Successfully cloned the card; returns the new card ID.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: The card does not exist or has been deleted.
            409:
                description: The card is currently locked or being processed by an AI assistant.
        """
        parent_id = card_id
        card = ModelCardEntry(ModelCard(), token2user.get(token, ""), conn)
        parent_card = find_card(card_id)
        with exists(parent_card, "Model card does not exist or has been deleted.") as src_card:
            try:
                card.card.data.assign(src_card.data)
            except AssertionError as e:
                logger.warn("Assertion error: " + str(e))
                abort(500, description=str(e))
            except Exception as e:
                logger.warn("Exception: " + str(e))
                abort(500, description=str(e))
        flattened = card.card.data.flatten()
        columns = list(flattened.keys())
        creator = token2user.get(token, "")
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
        with card_cache_lock:
            card_cache[card_id] = card
        logger.info("cloned a card", user=creator)
        return jsonify(card_id), 201

    @app.route(domain_prefix+'/assistants', methods=['GET'])
    @users.require_auth(token2expiration)
    def get_assistants(token: str):
        """
        Retrieves all available AI assistants for the current user and card, including their names and descriptions.
        ---
        tags:
          - UI
        responses:
            200:
                description: A list of assistants with their names and descriptions.
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        description: The name of the assistant.
                      desc:
                        type: string
                        description: The description of the assistant.
        """
        return jsonify([{"name": key, "desc": value.description} for key, value in assistants.items()])

    @app.route(domain_prefix+'/card/<int:card_id>', methods=['GET'])
    def get_card(card_id):
        """
        Retrieves the JSON data for a given model card.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The unique identifier for the model card.
        responses:
            200:
                description: The JSON representation of the model card.
                schema:
                  type: object
                  description: The model card contents. This includes fields title and a history graph.
            404:
                description: The requested card does not exist or has been deleted.
            409:
                description: An AI assistant is working on the model card.
        """
        found = find_card(card_id)
        with exists(found, "Model card does not exist or has been deleted.") as card:
            return jsonify(converters.dict2dynamic(card.data, {"title"})
                           |{"description": card.summary(), "quality": card.quality(), "history": found.history()})

    @app.route(domain_prefix+'/card/<int:card_id>/locked', methods=['GET'])
    def get_card_locked_status(card_id):
        """
        Retrieves a string value explaining why the card is locked, for example by an AI assistant working on it.
        If the card is locked, post or put methods on the card will create errors.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
        responses:
            200:
                description: The description (e.g., LLM progress stage) of the mechanism currently locking the card. An empty string if the card can be freely viewed or edited.
                schema:
                  type: string
            404:
                description: The request's card does not exist or has been deleted.
        """
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        return jsonify(card.check_completion())

    @app.route(domain_prefix+'/card/<int:card_id>/title', methods=['GET'])
    def get_card_title(card_id):
        """
        Retrieves the title of the specified model card.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
        responses:
            200:
                description: The title of the model card.
                schema:
                  type: string
            404:
                description: The requested card does not exist or has been deleted.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            return jsonify(card.title)

    @app.route(domain_prefix+'/card/<int:card_id>/title', methods=['PUT'])
    @users.require_auth(token2expiration)
    def set_card_title(card_id, token: str):
        """
        Updates the title of the specified model card.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's unique identifier.
          - name: body
            in: body
            required: true
            schema:
              type: string
              example: "New model card title"
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            200:
                description: The updated title of the model card.
                schema:
                  type: string
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: The requested card does not exist or has been deleted, or invalid request body.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card titles.")
            card.data['title'].set(json_data)
            return jsonify(card.data['title'])

    @app.route(domain_prefix+'/card/fields', methods=['GET'])
    def get_card_fields():
        """
        Lists all top-level field names for model cards that contain data entries.
        For example, this list does not contain the title but that it contains test datasets, training datasets, etc.
        This method helps the frontend be generalize-able in case there is a need for extensibility.
        Once fields are obtained, use /card/fields/<field_name> to retrieve its data entries.
        ---
        responses:
            200:
                description: List of top-level card field names.
                schema:
                    type: array
                    items:
                        type: string
        """
        return jsonify([key for key, value in empty_card.data.items() if isinstance(value, dict)])

    @app.route(domain_prefix+'/card/fields/<string:field_name>', methods=['GET'])
    def get_card_field_names(field_name):
        """
        Lists all data entry  names under the given field_name in a model card.
        ---
        parameters:
          - name: field_name
            in: path
            type: string
            required: true
            description: The top-level field name.
        responses:
            200:
                description: List of subfield names for the field.
                schema:
                    type: array
                    items:
                        type: string
            404:
                description: Field does not exist.
        """
        fields = empty_card.data
        field = exists(fields.get(field_name, None), f"Field '{field_name}' does not exist.")
        exists(isinstance(field, dict), f"Field '{field_name}' does not have data entries.")
        return jsonify(list(field.keys()))

    @app.route(domain_prefix+'/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['GET'])
    def get_card_field(card_id, field_name, data_name):
        """
        Retrieves an entry from card.field_name.data_name.
        For example, retrieve card.overview.version.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: field_name
            in: path
            type: string
            required: true
            description: The card's field name. To see all field names available for cards get /card/fields.
          - name: data_name
            in: path
            type: string
            required: true
            description: The data entry name within the card's field To see all data entries available for the field get /card/fields/field_name.
        responses:
            200:
                description: A string containing an editable (markdown) version of data values.
                schema:
                  type: string
                  description: The card's editable string representation.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            return jsonify(data)

    @app.route(domain_prefix+'/card/<int:card_id>/<string:field_name>/<string:data_name>', methods=['PUT'])
    @users.require_auth(token2expiration)
    def set_card_field(card_id, field_name, data_name, token: str):
        """
        Sets a value to card.field_name.data_name.
        ---
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: field_name
            in: path
            type: string
            required: true
            description: The card's field name. To see all field names available for cards get /card/fields.
          - name: data_name
            in: path
            type: string
            required: true
            description: The data entry name within the card's field To see all data entries available for the field get /card/fields/field_name.
          - name: body
            in: body
            required: true
            description: A string to set as value.
            schema:
              type: string
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            200:
                description: A list of integer identifiers.
                schema:
                    type: array
                    items:
                        type: integer
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: Resource does not exist, or invalid body.
            409:
                description: An AI assistant is working on the model card.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            field = exists(card.data.get(field_name, None), "Invalid field name. Candidates: " + ','.join(card.data.keys()))
            data = exists(field.get(data_name, None), f"Invalid data name {data_name}. Candidates: " + ','.join(field.keys()))
            json_data = request.get_json()
            exists(isinstance(json_data, str), "Can only send string data to update model card fields.")
            data.set(json_data)
            return jsonify(data.get())  # do not return json_data directly, as setting the value may format it


    @app.route(domain_prefix+'/card/<int:card_id>', methods=['DELETE'])
    @users.require_auth(token2expiration)
    def delete_card(card_id, token: str):
        """
        Removes the respective card; it will be considered a missing resource from now on.
        ---
        tags:
          - UI
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            204:
                description: Successfully removed.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: Resource does not exist.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as _:
            cursor = conn.conn.cursor()
            cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
            conn.conn.commit()
            with card_cache_lock: del card_cache[card_id]
            logger.info("deleted a card", user=token2user.get(token, None))
            return '', 204

    @app.route(domain_prefix+'/card/<int:card_id>', methods=['PUT'])
    @users.require_auth(token2expiration)
    def update_card(card_id, token: str):
        """
        Updates a model card's contents - enables manual upload.
        The provided json data should be (parts of) a model card's
        json representation with potentially some missing fields, and updates everything in the
        target card. The card's contents after setting everything are returned. This operation
        is safe in that all fields should be valid in order for any to be set.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: body
            in: body
            required: true
            description: Partial or full model card JSON to update the card with. This can be either in the dynamic format used by this API or in a static format that is exported by the aicard library.
            schema:
              type: object
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            200:
                description: Successfully set everything and retrieves a json representation of the model card.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: Either the card or at least one of the provided fields do not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        json_data = request.get_json()
        card_entry = find_card(card_id)
        with exists(card_entry, "Model card does not exist or has been deleted.") as card:
            try:
                assignable = converters.dynamic2dict(json_data, {"title"})
                card.data.assign(assignable)
                card.data.validate_integrity()
                card_entry.commit_card()
            except AssertionError as e: abort(404, "Wrong data: "+str(e))
            except Exception as e: abort(404, "Wrong data: "+str(e))
            logger.info("updated a card", user=token2user.get(token, None))
            return jsonify(converters.dict2dynamic(card.data, {"title"})
                           |{"description": card.summary(), "quality": card.quality(), "history": card_entry.history()})

    @app.route(domain_prefix+'/card', methods=['POST'])
    @users.require_auth(token2expiration)
    def create_card(token: str):
        """
        Creates a model card given an optional json representation - the representation is for manual upload.
        The provided json data should be either an empty dict or (parts of) a model card's
        json representation with potentially some missing fields, and updates everything in the
        target card. The card's contents after setting everything are retrieved.
        ---
        tags:
          - UI
        parameters:
          - name: body
            in: body
            required: false
            schema:
              type: object
              description: Binary encoding of a file loading the card.
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            201:
                description: Successfully set everything and retrieves a json representation of the model card.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: One of the provided fields do not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        json_data = request.get_json()
        card = ModelCardEntry(ModelCard(), token2user.get(token, ""), conn)
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
        creator = token2user.get(token, "")
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
    @users.require_auth(token2expiration)
    def autocomplete_card(card_id: int, assistant_type: str, token: str):
        """
        Autocompletes an already created model card given a string pointing to a repository URL or some file contents.
        This calls on an AI assistant to work on the card, blocking editing while the latter runs.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: assistant_type
            in: path
            type: string
            required: true
            description: The AI assistant type. Options available from get /assistants.
          - name: body
            description: A repository url starting with http:// or https://, or an uploaded readme text file's contents (can be the contents of a .txt, .md, or .html file).
            in: body
            required: true
            schema:
              type: string
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            200:
                description: Successfully submitted task.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        card = exists(find_card(card_id), "Model card does not exist or has been deleted.")
        
        if 'file' in request.files:
            uploaded_file = request.files['file']
            exists(uploaded_file.filename != "", "Empty file uploaded")
            file_bytes = uploaded_file.read(5)
            uploaded_file.seek(0)
            if file_bytes == b"%PDF-":
                data_type = 'pdf'
            else:
                abort(415, description="Unsupported file type.")
            tmp_file = uploaded_file.filename # files delete in card.autocomplete thread
            uploaded_file.save(tmp_file)
            
            json_data = {"data_type": data_type, "path": tmp_file}
        else:
            json_data = {"data_type": "url", "url": request.get_json()}
            exists(isinstance(json_data['url'], str), "Autocomplete requires a url string as POST data")
            
        status = card.autocomplete(json_data, assistant, logger)
        logger.info(f"requested card {card_id} autocompletion from {assistant_type}", user=token2user.get(token, None))

        return jsonify(status)

    @app.route(domain_prefix+'/assistant/<string:assistant_type>/refine/<int:card_id>', methods=['POST'])
    @users.require_auth(token2expiration)
    def autorefine_card(card_id: int, assistant_type: str, token: str):
        """
        Refines an already created model card so that its contents are easier to parse by laypeople.
        This calls on an AI assistant to work on the card, blocking editing while the latter runs.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: assistant_type
            in: path
            type: string
            required: true
            description: The AI assistant type. Options available from get /assistants.
          - name: Authorization
            in: header
            type: string
            required: true
            description: Bearer token for user authentication (e.g., "Bearer <token>")
        responses:
            200:
                description: Successfully submitted task.
            401:
                description: Unauthorized — missing token or invalid token format.
            403:
                description: Unauthorized — token expired or not valid.
            404:
                description: Resource does not exist.
            409:
                description: An AI assistant is working on the model card.
        """
        assistant = exists(assistants.get(assistant_type, None), "Assistant not available")
        status = exists(find_card(card_id), "Model card does not exist or has been deleted.").autorefine(assistant, logger)
        logger.info(f"requested card {card_id} refinement from {assistant_type}", user=token2user.get(token, None))
        return jsonify(status)

    @app.route(domain_prefix+"/card/<int:card_id>/download/<string:fformat>", methods=["GET"])
    def download_card(card_id, fformat):
        """
        Download a model card.
        ---
        tags:
          - UI
        parameters:
          - name: card_id
            in: path
            type: integer
            required: true
            description: The card's identifier.
          - name: fformat
            in: path
            type: string
            required: true
            description: The download format. Must be 'json' or 'markdown'.
        responses:
            200:
                description: Successfully downloaded the model card.
            400:
                description: Invalid format. Must be 'json' or 'markdown'.
            404:
                description: Model card does not exist or has been deleted.
        """
        with exists(find_card(card_id), "Model card does not exist or has been deleted.") as card:
            if fformat == "json":
                content = json.dumps(converters.dict2dynamic(card.data, {"title"})).encode('utf-8')
                filename = f"{card.title}.json"
                mimetype = "text/html"
            elif fformat == "markdown":
                content = card.to_markdown().encode('utf-8')
                filename = f"{card.title}.md"
                mimetype = "text/html"
            elif fformat == "pdf":
                html_content = card.to_html()+ """
                    <style>
                    body {
                        margin: 1cm;
                        font-size: 12px;
                        word-wrap: break-word;
                    }
                    img {
                        max-width: 100%;
                        height: auto;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        table-layout: fixed;
                        font-size: 11px;
                    }
                    th, td {
                        word-wrap: break-word;
                        overflow-wrap: break-word;
                        text-overflow: ellipsis;
                        padding: 4px;
                        border: 1px solid #ccc;
                    }
                    </style>
                    """
                from weasyprint import HTML

                pdf_io = BytesIO()
                HTML(string=html_content).write_pdf(pdf_io)
                pdf_io.seek(0)
                content = pdf_io.read()
                filename = f"card_{card_id}.pdf"
                mimetype = "application/pdf"
                filename = f"{card.title}.pdf"
            else:
                abort(400, description="Invalid format. Must be 'json', 'markdown', or 'pdf.")

        return Response(
            content,
            mimetype=mimetype,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    @app.route(domain_prefix+"/options/<string:section>/<string:field>", methods=["GET"])
    def get_options(section, field):
        try:
            return jsonify(ModelCard().data[section][field].options())
        except Exception as e:
            logger.error("No options for" + section + " " + field)
            abort(400, "No options for" + section + " " + field)
            
        

    @app.route(domain_prefix+'/docs', methods=['GET'])
    def docs():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':  continue
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            routes.append({
                "endpoint": rule.endpoint,
                "methods": methods,
                "path": str(rule),
            })
        return jsonify(routes)

    def gc():
        while True:
            now = time.time()
            one_hour = 3600
            to_delete = []
            with card_cache_lock:
                for card_id, entry in list(card_cache.items()):
                    if entry is None:
                        to_delete.append(card_id)
                        continue
                    with entry.lock:
                        if not entry._is_completing and now - entry.last_accessed > one_hour:
                            to_delete.append(card_id)
                for card_id in to_delete: card_cache.pop(card_id, None)
            time.sleep(600)  # run every 10 minutes

    logger.ok("Server is ready: http://127.0.0.1:5000"+domain_prefix)
    return app, gc
