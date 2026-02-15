import bcrypt
import hashlib

class Hash:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt. 
        We use SHA256 first to ensure we never hit bcrypt's 72-character limit.
        """
        sha256_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        pwd_bytes = sha256_hash.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain text password against a bcrypt hash.
        """
        try:
            sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
            pwd_bytes = sha256_hash.encode("utf-8")
            return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
        except Exception:
            return False