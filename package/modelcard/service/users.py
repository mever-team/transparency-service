import sqlite3
import bcrypt
from functools import wraps
from flask import request, abort, Response
import time
import os

def init_user_dbs(root="db"):
    os.makedirs(root, exist_ok=True)
    for db_name in [os.path.join(root, 'users.db'), os.path.join(root, 'pending_users.db')]:
        conn = sqlite3.connect(db_name)
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )''')
        conn.commit()
        conn.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def find_user(db_path, username):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT username, email, password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def insert_user(db_path, username, email, password):
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                 (username, email, hash_password(password)))
    conn.commit()
    conn.close()

def require_auth(token2expiration: dict):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "): abort(401, description="Missing token")
            token_parts = auth.split()
            if len(token_parts) != 2: abort(401, description="Invalid token format")
            token = token_parts[1]
            expiry = token2expiration.get(token)
            if not expiry or time.time() > expiry: abort(403, description="Token expired or invalid")
            return f(*args, **kwargs)
        return wrapper
    return decorator

def admin_auth_required(token2expiration: dict):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth or not isinstance(auth, str):return Response("Missing Authorization header", 401)
            parts = auth.strip().split()
            if len(parts) != 2 or parts[0] != "Bearer": return Response("Invalid Authorization format", 401)
            token = parts[1]
            expiry = token2expiration.get(token)
            if not expiry or time.time() > expiry: return Response("Invalid or expired bearer token", 403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
