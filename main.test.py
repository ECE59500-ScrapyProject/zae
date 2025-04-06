import unittest
from zae import ZAE

class TestAuthMethods(unittest.TestCase):
    def setUp(self):
        self.zae = ZAE()  # Create an instance of the ZAE class
        self.user_id = "user123"
        self.jwt_secret = "my_jwt_secret"
        self.user_password = "user_password"
        self.wrong_password = "wrong_password"
        self.token_data = '{"user_id": "' + self.user_id + '", "exp": "2023-12-31T23:59:59"}'

    def test_generate_and_verify_jwt(self):
        # Test JWT generation
        jwt_token = self.zae.generate_jwt(self.user_id, self.jwt_secret)
        self.assertIsInstance(jwt_token, str)
        
        # Test JWT verification
        verified_payload = self.zae.verify_jwt(jwt_token, self.jwt_secret)
        self.assertIn("user_id", verified_payload)
        self.assertEqual(verified_payload["user_id"], self.user_id)

    def test_encrypt_and_decrypt_token_correct_password(self):
        # Test token encryption
        encrypted_token = self.zae.encrypt_token(self.token_data, self.user_password)
        self.assertIsInstance(encrypted_token, bytes)
        
        # Test token decryption with correct password
        decrypted_token = self.zae.decrypt_token(encrypted_token, self.user_password)
        self.assertEqual(decrypted_token, self.token_data)

    def test_decrypt_token_incorrect_password(self):
        # Test token decryption with incorrect password
        encrypted_token = self.zae.encrypt_token(self.token_data, self.user_password)
        with self.assertRaises(ValueError) as context:
            self.zae.decrypt_token(encrypted_token, self.wrong_password)
        self.assertEqual(
            str(context.exception),
            "Decryption failed. Ensure the password is correct and the token is valid."
        )
        

if __name__ == "__main__":
    unittest.main()