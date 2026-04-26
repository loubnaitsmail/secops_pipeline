import pytest
import sys
sys.path.append('./app')
from main import hash_password, get_user

def test_hash_password():
    """Test que la fonction hash retourne quelque chose"""
    result = hash_password("password123")
    assert result is not None
    assert len(result) > 0

def test_get_user_returns_none():
    """Test avec un utilisateur inexistant"""
    result = get_user("utilisateur_inexistant")
    assert result is None
