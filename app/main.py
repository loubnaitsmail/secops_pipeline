import sqlite3
import hashlib
import os

# A02 - Secret hardcodé
SECRET_KEY = "mysecretkey123"
API_TOKEN = "ghp_abc123def456"

def get_db():
    conn = sqlite3.connect("users.db")
    return conn

def get_user(username):
    """A03 - Injection SQL"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

def login(username, password):
    """A03 - Injection SQL dans le login"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    return cursor.fetchone() is not None

def hash_password(password):
    """A02 - Algorithme obsolète SHA1"""
    return hashlib.sha1(password.encode()).hexdigest()

def get_user_by_id(user_id):
    """A01 - Pas de vérification d'autorisation"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    return cursor.fetchone()

def delete_user(user_id):
    """A03 - Injection SQL dans suppression"""
    conn = get_db()
    cursor = conn.cursor()
    query = "DELETE FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    conn.commit()
