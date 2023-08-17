from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import json
import base64

# Dados da chave
password = b"supersecret"  # A senha usada para derivar a chave

# Ler os dados do arquivo JSON
with open("message.json", "r") as arquivo_json:
    encrypted_data = json.load(arquivo_json)

# Decodificar os dados de Base64
ciphertext = base64.b64decode(encrypted_data["ciphertext"])
salt = base64.b64decode(encrypted_data["salt"])

# Derivar a chave do PBKDF2 usando o salt e iterações fornecidos anteriormente
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # Tamanho da chave AES em bytes
    salt=salt,
    iterations=encrypted_data["iterations"]
)
key = kdf.derive(password)

# Usar AES para desencriptar a mensagem
cipher = Cipher(algorithms.AES(key), modes.ECB()) 
decryptor = cipher.decryptor()
decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Remover o padding
unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

print("Mensagem desencriptada:", decrypted_message.decode("utf-8"))  # Converta para string
