import random
import hashlib

from utils.config_parser import config
from auth.authModel import get_user


def generate_salt():
    """Generates a random salt string for password."""
    salt = ''.join(random.choice(config()['base']['ascii_and_digits']) for _ in range(16))
    return salt


def hash_sha256_password(password, salt = ''):
    """Hashes the password with SHA256."""
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode('utf-8'))
    if salt:
        salt = salt
    else:
        salt = generate_salt()
    hash_obj.update(salt.encode('utf-8'))
    hash_obj.update(config()["auth"]["secret_key"].encode('utf-8'))
    return f"{hash_obj.hexdigest()}{salt}"


def get_hashed_password(email, password):
    """Get salt and generate hashed client secret"""
    row = get_user(email)

    salt = row[2][-16:]
    hashed_secret = hash_sha256_password(password, salt)
    return hashed_secret
