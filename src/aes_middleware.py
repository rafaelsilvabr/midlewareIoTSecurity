from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

class AESMiddleware:
    def __init__(self, password):
        self.password = password
        self.key = self.generate_key()
    @classmethod
    def from_default(cls):
        return cls("null")

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
        return key


    def encrypt(self, message):
        # Configurar o padding para a mensagem
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message) + padder.finalize()

        # Usar AES para encriptar a mensagem
        cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        encrypted_data = {
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "salt": base64.b64encode(salt).decode("utf-8"),
            "iterations": 100000
        }

        return encrypted_data

    def decrypt(self, encrypted_message):
        backend = default_backend()

        # Decodificar a mensagem encriptada de base64
        encrypted_bytes = base64.b64decode(encrypted_message)

        # Extrair o IV (primeiros 16 bytes)
        iv = encrypted_bytes[:16]

        # Resto dos bytes são o texto cifrado
        ciphertext = encrypted_bytes[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=backend)
        decryptor = cipher.decryptor()

        # Decifrar o texto cifrado
        decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

        # Remover o padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_message_bytes = unpadder.update(decrypted_padded_message) + unpadder.finalize()

        # Decodificar os bytes da mensagem para string
        decrypted_message = decrypted_message_bytes.decode("utf-8")

        return decrypted_message

# Criar uma instância da classe AESMiddleware com a senha
##password = "senha_super_secreta"
##aes_middleware = AESMiddleware()
##aes_device = aes_middleware.generate_device(password)

# Mensagem a ser criptografada
##message = "Esta é uma mensagem secreta!"

# Criptografar a mensagem
##encrypted_message = aes_middleware.encrypt(message)
##print("Mensagem criptografada:", encrypted_message)

# Descriptografar a mensagem
##decrypted_message = aes_middleware.decrypt(encrypted_message)
##print("Mensagem descriptografada:", decrypted_message)
