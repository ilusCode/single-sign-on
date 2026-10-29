from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return _password_hasher.hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        # InvalidHashError: the stored value is not an Argon2 hash (e.g. a legacy plain-text password)
        return False
