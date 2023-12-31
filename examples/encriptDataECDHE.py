from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

def encrypt_ECDHE(message, key):
    backend = default_backend()
    iv = os.urandom(16)  # Initialization vector (16 bytes)

    # Transformar a mensagem em bytes usando UTF-8
    message_bytes = message.encode("utf-8")

    # Pad the message to be a multiple of the block size
    padder = padding.PKCS7(algorithms.Camellia.block_size).padder()
    padded_message = padder.update(message_bytes) + padder.finalize()

    cipher = Cipher(algorithms.Camellia(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return iv + ciphertext

# Chave Camellia em formato Base64URL (44 caracteres)
base64_url_key = "aRnEFjIiYerS3FOFIUn-kHbHAy-vUfXIDlMXJUg54V4="
key_bytes = base64.urlsafe_b64decode(base64_url_key)  # Decodifica Base64URL para bytes

# Mensagem a ser encriptada
message = "Esta é uma mensagem secreta!"

# Encriptar a mensagem
encrypted_message = encrypt_ECDHE(message, key_bytes)

# Converter a mensagem encriptada para base64
base64_encrypted_message = base64.b64encode(encrypted_message)

print("Mensagem encriptada:", base64_encrypted_message.decode("utf-8"))
