import pytest
import sqlite3
import sys
sys.path.append('./app')
from main import hash_password, get_user, login, delete_user

@pytest.fixture
def db(monkeypatch):
    """
    Fixture : crée une BDD temporaire en mémoire pour chaque test.
    - ':memory:' = BDD SQLite qui vit uniquement en RAM
    - Créée avant chaque test, détruite après
    - Jamais écrite sur le disque
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Crée la table users avec la même structure que la vraie BDD
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)

    # Insère un utilisateur de test
    cursor.execute(
        "INSERT INTO users VALUES (1, 'alice', 'hashed_password')"
    )
    conn.commit()

    # monkeypatch remplace get_db() par notre BDD temporaire
    # pour que les fonctions de main.py utilisent cette BDD de test
    import main
    monkeypatch.setattr(main, "get_db", lambda: conn)

    yield conn
    conn.close()


def test_hash_password():
    """Test que SHA256 retourne un hash de 64 caractères"""
    result = hash_password("password123")
    assert result is not None
    assert len(result) == 64  # SHA256 = toujours 64 caractères


def test_get_user_exists(db):
    """Test qu'on trouve un utilisateur existant"""
    result = get_user("alice")
    assert result is not None
    assert result[1] == "alice"


def test_get_user_not_found(db):
    """Test qu'un utilisateur inexistant retourne None"""
    result = get_user("utilisateur_inexistant")
    assert result is None


def test_login_success(db):
    """Test d'un login réussi"""
    result = login("alice", "hashed_password")
    assert result is True


def test_login_failure(db):
    """Test d'un login échoué"""
    result = login("alice", "mauvais_mot_de_passe")
    assert result is False


def test_delete_user(db):
    """Test de suppression d'un utilisateur"""
    delete_user(1)
    result = get_user("alice")
    assert result is None
