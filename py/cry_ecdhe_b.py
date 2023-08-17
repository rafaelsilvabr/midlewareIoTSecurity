from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import json
import base64

# Ler os dados do arquivo JSON
with open("keys.json", "r") as arquivo_json:
    keys = json.load(arquivo_json)

# Ler os dados do arquivo JSON
with open("message_ecdhe.json", "r") as arquivo_json:
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
shared_key_b = base64.b64decode(keys["shared_key"])
encryption_key = kdf.derive(shared_key_b)

# Usar AES para desencriptar a mensagem
cipher = Cipher(algorithms.AES(encryption_key), modes.ECB()) 
decryptor = cipher.decryptor()
decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Remover o padding
unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

print("Mensagem desencriptada:", decrypted_message.decode("utf-8"))  # Converta para string
