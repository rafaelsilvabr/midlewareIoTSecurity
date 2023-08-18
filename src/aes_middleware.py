from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class AESMiddleware:
    def __init__(self, password):
        self.password = password
        self.key = self.generate_key()

    def generate_key(self):
        password_bytes = self.password.encode()
        salt = b'\x85e^\xb4\xbc\\\x16\x03\xcf\x94Ou\x18\x03\xd7\x98'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=salt,
            length=32,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        print("DEBUG AESMDW GENERATEKEY")
        print(key)
        return key


    def encrypt(self, message):
        cipher = Fernet(self.key)
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    def decrypt(self, encrypted_message):
        cipher = Fernet(self.key)
        decrypted_message = cipher.decrypt(encrypted_message).decode()
        return decrypted_message

# Criar uma instância da classe AESMiddleware com a senha
password = "senha_super_secreta"
aes_middleware = AESMiddleware(password)

# Mensagem a ser criptografada
message = "Esta é uma mensagem secreta!"

# Criptografar a mensagem
encrypted_message = aes_middleware.encrypt(message)
print("Mensagem criptografada:", encrypted_message)

# Descriptografar a mensagem
decrypted_message = aes_middleware.decrypt(encrypted_message)
print("Mensagem descriptografada:", decrypted_message)
