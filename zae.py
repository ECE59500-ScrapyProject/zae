import jwt
import datetime
from cryptography.fernet import Fernet
import base64
import hashlib

class ZAE:
    # ===============================
    # Traditional JWT Implementation
    # ===============================
    def generate_jwt(self, user_id, secret_key):
        """
        Generate a JWT token with a simple payload.
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    def verify_jwt(self, token, secret_key):
        """
        Verify the JWT token. Return payload if valid, else None.
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("JWT Token expired.")
            return None
        except jwt.InvalidTokenError:
            print("Invalid JWT Token.")
            return None

    # ============================================
    # Zero-Access Encryption (ZAE) Implementation
    # ============================================
    def derive_key(self, password):
        """
        Derive a 32-byte key from a password using SHA256.
        Fernet requires a base64-encoded 32-byte key.
        """
        digest = hashlib.sha256(password.encode()).digest()
        key = base64.urlsafe_b64encode(digest)
        return key

    def encrypt_token(self, token_data, password):
        """
        Encrypt the token data using a key derived from the user's password.
        """
        key = self.derive_key(password)  # Derive the encryption key from the password
        f = Fernet(key)  # Create a Fernet instance with the derived key
        token_bytes = token_data.encode()  # Convert the token data to bytes
        encrypted_token = f.encrypt(token_bytes)  # Encrypt the token data
        return encrypted_token
    
    def decrypt_token(self, encrypted_token, password):
        """
        Decrypt the token. Without the correct password, decryption fails.
        """
        key = self.derive_key(password)  # Derive the decryption key from the password
        f = Fernet(key)  # Create a Fernet instance with the derived key
        try:
            decrypted_bytes = f.decrypt(encrypted_token)  # Attempt to decrypt the token
            return decrypted_bytes.decode()  # Decode the decrypted bytes back to a string
        except Exception as e:
            raise ValueError("Decryption failed. Ensure the password is correct and the token is valid.") from e

    