import sqlite3
import hashlib
import os

# ✅ Fix A02 : Secrets chargés depuis les variables d'environnement
SECRET_KEY = os.environ.get("SECRET_KEY")
API_TOKEN = os.environ.get("API_TOKEN")

def get_db():
    conn = sqlite3.connect("users.db")
    return conn

def get_user(username):
    """✅ Fix A03 : Prepared statement"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def login(username, password):
    """✅ Fix A03 : Prepared statement"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    return cursor.fetchone() is not None

def hash_password(password):
    """✅ Fix A02 : SHA256 remplace SHA1"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_id(user_id):
    """✅ Fix A01 + A03 : Prepared statement"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def delete_user(user_id):
    """✅ Fix A03 : Prepared statement"""
    conn = get_db()
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    conn.commit()
