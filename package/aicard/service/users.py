from functools import wraps
from flask import request, abort, Response
from aicard.card import ModelCard
import sqlite3
import bcrypt
import time
import os
import atexit
import sys
import jwt
from jwt import PyJWKClient


def hash_password(password: str) -> str:
    if not password: return password
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    if not password or not hashed: return False
    return bcrypt.checkpw(password.encode(), hashed.encode())

class UserDB:
    def __init__(self, logger, root:str="db", admin_name:str="admin", admin_password:str="admin", admin_email:str=""): # pragma: no cover
        if not root:
            logger.info("Initializing non-persistent testing database")
            conn = sqlite3.connect(":memory:", check_same_thread=True)
            self.db_path = None
        else:
            os.makedirs(root, exist_ok=True)
            self.db_path = os.path.join(root, "auth.db")
            conn = sqlite3.connect(self.db_path, check_same_thread=True)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode=WAL;")

        # create user tables
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS pending_users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )''')

        # create report table
        conn.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY(card_id) REFERENCES cards(id) ON DELETE CASCADE
        )''')

        # create model card table
        prototype = ModelCard()
        col_names = list(prototype.data.flatten().keys())
        assert "user" not in col_names and "id" not in col_names and "desc" not in col_names and "timestamp" not in col_names and "quality" not in col_names and "report_count" not in col_names, \
            "The ModelCard schema cannot be defined to include id, user, desc, timestamp, quality, or report_count fields at the top level, since these are externally managed by the service database"
        col_defs = ",\n    ".join([f'"{col}" TEXT' for col in col_names])
        create_cards_table = f'''CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            desc TEXT NOT NULL,
            quality DOUBLE,
            timestamp INT,
            {col_defs},
            FOREIGN KEY(user) REFERENCES users(username) ON DELETE CASCADE
        )'''
        conn.execute(create_cards_table)

        # maintenance - TODO: REMOVE THIS SNIPPET IN FUTURE SERVER VERSIONS
        existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(cards)").fetchall()}
        if "quality" not in existing_cols:
            conn.execute("ALTER TABLE cards ADD COLUMN quality DOUBLE")
        if "timestamp" not in existing_cols:
            conn.execute("ALTER TABLE cards ADD COLUMN timestamp INTEGER")

        # maintenance - TODO: REMOVE THIS SNIPPET IN FUTURE SERVER VERSIONS
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card_children'")
        exists = cursor.fetchone() is not None
        if exists and not conn.execute("SELECT COUNT(*) FROM card_children").fetchone()[0]:
            conn.execute("DROP TABLE card_children")

        # maintenance - TODO: REMOVE THIS SNIPPET IN FUTURE SERVER VERSIONS
        if "report_count" not in existing_cols:
            conn.execute('ALTER TABLE cards ADD COLUMN report_count INTEGER NOT NULL DEFAULT 0')

        # create card children table
        conn.execute('''CREATE TABLE IF NOT EXISTS card_children (
            parent_id INTEGER NOT NULL,
            child_id INTEGER NOT NULL,
            message TEXT DEFAULT '',
            FOREIGN KEY(parent_id) REFERENCES cards(id) ON DELETE CASCADE,
            FOREIGN KEY(child_id) REFERENCES cards(id) ON DELETE CASCADE,
            PRIMARY KEY(parent_id, child_id)
        )''')

        conn.execute('''
        CREATE INDEX IF NOT EXISTS idx_card_children_child
        ON card_children(child_id)
        ''')

        conn.execute('''
        CREATE TRIGGER IF NOT EXISTS card_children_rewire_parent_deleted
        BEFORE DELETE ON card_children
        WHEN OLD.parent_id != OLD.child_id
          AND NOT EXISTS (SELECT 1 FROM cards WHERE id = OLD.parent_id)
        BEGIN
            INSERT OR IGNORE INTO card_children (parent_id, child_id, message)
            SELECT
                cc.parent_id,
                OLD.child_id,
                cc.message
            FROM card_children AS cc
            WHERE cc.child_id = OLD.parent_id
              AND cc.parent_id != OLD.child_id;
        END;
        ''')

        conn.execute('''
        CREATE TRIGGER IF NOT EXISTS card_children_rewire_child_deleted
        BEFORE DELETE ON card_children
        WHEN OLD.parent_id != OLD.child_id
          AND NOT EXISTS (SELECT 1 FROM cards WHERE id = OLD.child_id)
        BEGIN
            INSERT OR IGNORE INTO card_children (parent_id, child_id, message)
            SELECT
                OLD.parent_id,
                cc.child_id,
                cc.message
            FROM card_children AS cc
            WHERE cc.parent_id = OLD.child_id
              AND cc.child_id != OLD.parent_id;
        END;
        ''')

        # report counting (INVARIANCE: CAN ONLY INSERT OR DELETE REPORTS)
        conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS reports_ai AFTER INSERT ON reports
        BEGIN
            UPDATE cards SET report_count = report_count + 1
            WHERE id = NEW.card_id;
        END;
        """)
        conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS reports_ad AFTER DELETE ON reports
        BEGIN
            UPDATE cards SET report_count = report_count - 1
            WHERE id = OLD.card_id;
        END;
        """)

        # automatic migration if needed
        expected_columns = ['id', 'user', 'desc', 'quality', 'timestamp', 'report_count'] + col_names
        cursor = conn.execute("PRAGMA table_info(cards)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        missing = [col for col in expected_columns if col not in existing_columns]
        redundant = [col for col in existing_columns if col not in expected_columns]

        if missing or redundant:
            logger.warn("The prototype for ModelCard does not match the database schema of cards. Migrating...")
            if missing:
                logger.warn(f"Adding missing columns: {', '.join(missing)}")
                for col in missing:
                    conn.execute(f'ALTER TABLE cards ADD COLUMN "{col}" TEXT')
            if redundant:
                logger.warn(f"The following columns are leftover and will be removed: {', '.join(redundant)}")
                print("To proceed with removing leftover columns, type 'migrate' and press Enter. Otherwise delete the database file")
                user_input = input(">> ").strip().lower()
                if user_input != "migrate":
                    logger.error("Migration cancelled. Please review the ModelCard schema.")
                    sys.exit(1)
                # SQLite doesn't support DROP COLUMN directly. So we recreate the table:
                temp_cols = [col for col in existing_columns if col not in redundant]
                temp_col_str = ', '.join([f'"{col}"' for col in temp_cols])
                conn.execute("BEGIN")
                conn.execute(f'CREATE TABLE cards_new AS SELECT {temp_col_str} FROM cards')
                conn.execute('DROP TABLE cards')
                conn.execute(create_cards_table)
                insert_cols = ', '.join(temp_cols)
                select_cols = ', '.join(temp_cols)
                conn.execute(f'INSERT INTO cards ({insert_cols}) SELECT {select_cols} FROM cards_new')
                conn.execute('DROP TABLE cards_new')
                conn.commit()
            else: logger.info("There are no leftover columns to be removed")
            conn.execute("DROP TABLE IF EXISTS cards_fts")
            logger.info("Rebuilding inverse search index")

        # create inverse index table
        fts_cols = ['desc'] + col_names  # desc + all dynamic ModelCard fields
        fts_col_defs = ",\n    ".join([f'"{col}"' for col in fts_cols])
        create_fts = f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS cards_fts USING fts5(
            {fts_col_defs},
            content='cards',
            content_rowid='id',
            tokenize='trigram'
        );
        """
        conn.execute(create_fts)

        # automatic synchronization triggers (avoids book-keeping from our end)
        conn.executescript(f"""
        CREATE TRIGGER IF NOT EXISTS cards_ai AFTER INSERT ON cards BEGIN
          INSERT INTO cards_fts(rowid, {', '.join(fts_cols)})
          VALUES (new.id, {', '.join(['new.' + c for c in fts_cols])});
        END;

        CREATE TRIGGER IF NOT EXISTS cards_ad AFTER DELETE ON cards BEGIN
          INSERT INTO cards_fts(cards_fts, rowid, {', '.join(fts_cols)})
          VALUES('delete', old.id, {', '.join(['old.' + c for c in fts_cols])});
        END;

        CREATE TRIGGER IF NOT EXISTS cards_au AFTER UPDATE ON cards BEGIN
          INSERT INTO cards_fts(cards_fts, rowid, {', '.join(fts_cols)})
          VALUES('delete', old.id, {', '.join(['old.' + c for c in fts_cols])});
          INSERT INTO cards_fts(rowid, {', '.join(fts_cols)})
          VALUES (new.id, {', '.join(['new.' + c for c in fts_cols])});
        END;
        """)

        conn.commit()
        atexit.register(conn.close)
        self.conn = conn
        if root == 'db_pytest':
            self.insert_user("users", "pytest", "", "pytest")
            logger.info("Test run detected. Initializing pytest user.\n * name: pytest\n * password: pytest")
        if not self.find_user("users", admin_name):
            self.insert_user("users", admin_name, admin_email, admin_password)
            logger.info("First time run detected.")
            logger.ok(f"Created database and administrator user with default credentials.\n * name: {admin_name}\n * password: {admin_password}")
            logger.warn("REMEMBER TO CHANGE THE DEFAULT ADMINISTRATOR PASSWORD")
        else: logger.ok("Database loaded.")

    def find_user(self, table: str, username: str):
        cursor = self.conn.execute(
            f"SELECT username, email, password FROM {table} WHERE username = ?",
            (username,)
        )
        return cursor.fetchone()

    def insert_user(self, table_name: str, username: str, email: str, password: str, commit: bool=True):
        self.conn.execute(
            f"INSERT INTO {table_name} (username, email, password) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        if commit: self.conn.commit()

    def create_card_relation(self, parent_id: int, child_id: int, message: str):
        cursor = self.conn.execute(
            "SELECT 1 FROM card_children WHERE parent_id = ? AND child_id = ?",
            (parent_id, child_id)
        )
        exists = cursor.fetchone() is not None
        if exists:
            self.conn.execute(
                "UPDATE card_children SET message = ? WHERE parent_id = ? AND child_id = ?",
                (message, parent_id, child_id)
            )
        else:
            self.conn.execute(
                "INSERT INTO card_children (parent_id, child_id, message) VALUES (?, ?, ?)",
                (parent_id, child_id, message)
            )
        self.conn.commit()
class CookieAuthenticator:
    def __init__(self, ISSUER, AUDIENCE, CERT, register_token, timeout_seconds=3, logger=None):
        self.ISSUER = ISSUER.rstrip("/")
        self.AUDIENCE = AUDIENCE
        self.register_token = register_token
        self.jwks_client = PyJWKClient(CERT.rstrip("/"))
        self.logger = logger
        self.timeout_seconds = timeout_seconds

    def validate_token(self, token: str, unsafely_skip_verification=False):
        """Returns either an empty dict (if the token could not be verified) or a dict of verified information.
        Pass unsafely_skip_verification=True if you have external means of verifying the token issuer.
        IN THAT CASE, THE TOKEN IS NOT VERIFIED WITH THE ISSUER."""
        if not token:
            if self.logger: self.logger.warn("No token to validate")
            return {}
        try:
            header = jwt.get_unverified_header(token)
            if not header.get("kid"):
                jwks = self.jwks_client.get_jwk_set()
                for key in jwks.keys:
                    try:
                        claims = jwt.decode(
                            token,
                            key.key,
                            algorithms=header.get("alg", "RS256"),
                            audience=self.AUDIENCE,
                            issuer=self.ISSUER,
                            leeway=10,
                            timeout=self.timeout_seconds
                        )
                        return {
                            "email": claims.get("email"),
                            "preferred_username": claims.get("preferred_username"),
                            "given_name": claims.get("given_name"),
                            "family_name": claims.get("family_name"),
                        }
                    except jwt.InvalidSignatureError:
                        continue
                if unsafely_skip_verification: return header
                if self.logger: self.logger.error("Unverify-able header without \"kid\" field: " + str(header))
                return {}
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=header.get("alg", "RS256"),
                audience=self.AUDIENCE,
                issuer=self.ISSUER,
                leeway=10,
                timeout=self.timeout_seconds
            )
            return {
                "email": claims.get("email"),
                "preferred_username": claims.get("preferred_username"),
                "given_name": claims.get("given_name"),
                "family_name": claims.get("family_name"),
            }
        except jwt.ExpiredSignatureError: abort(401, "Token expired")
        except jwt.InvalidAudienceError: abort(401, "Invalid audience")
        except jwt.InvalidIssuerError: abort(401, "Invalid issuer")
        except jwt.InvalidTokenError: abort(401, "Invalid token")

def require_auth(token2expiration: dict, third_party_authenticator: CookieAuthenticator|None=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer ") and third_party_authenticator:
                token = request.cookies.get("access_token")
                payload = third_party_authenticator.validate_token(token)
                if payload:
                    username = payload.get("username")
                    email = payload.get("email")
                    if not username: abort(401, description="Invalid cookie payload")
                    third_party_authenticator.register_token(token, username, email)
                    token2expiration[token] = time.monotonic() # we allow always, so expire immediately
                    return f(*args, **kwargs, token=token)
            # continue with normal internal validation
            if not auth.startswith("Bearer "): abort(401, description="Missing token")
            parts = auth.strip().split()
            if len(parts) != 2 or parts[0] != "Bearer": abort(401, description="Invalid token format")
            token = parts[1]
            expiry = token2expiration.get(token)
            if not expiry or time.monotonic() > expiry: abort(403, description="Token expired or invalid - please log in")
            return f(*args, **kwargs, token=token)
        return wrapper
    return decorator

def require_admin(token2expiration: dict):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth or not isinstance(auth, str): abort(401, description="Invalid token format")
            parts = auth.strip().split()
            if len(parts) != 2 or parts[0] != "Bearer": abort(403, description="Token expired or invalid - please log in")
            token = parts[1]
            expiry = token2expiration.get(token)
            if not expiry or time.monotonic() > expiry: abort(403, description="Token expired or invalid - please log in")
            return f(*args, **kwargs, token=token)
        return wrapper
    return decorator
