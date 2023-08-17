from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import json
import base64

# Dados da chave
password = b"supersecret"  # A senha usada para derivar a chave
salt = b"some_salt"  # O salt usado para derivação de chave
iterations = 100000  # Número de iterações do PBKDF2

# Derivar a chave do PBKDF2
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # Tamanho da chave AES em bytes
    salt=salt,
    iterations=iterations
)
key = kdf.derive(password)

# Mensagem a ser encriptada
message = b"Boa tarde!"

# Configurar o padding para a mensagem
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_message = padder.update(message) + padder.finalize()

# Usar AES para encriptar a mensagem
cipher = Cipher(algorithms.AES(key), modes.ECB()) 
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_message) + encryptor.finalize()

# Serializar a mensagem encriptada e outros parâmetros relevantes
encrypted_data = {
    "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    "salt": base64.b64encode(salt).decode("utf-8"),
    "iterations": iterations
}

# Salvar os dados no arquivo JSON
with open("message.json", "w") as arquivo_json:
    json.dump(encrypted_data, arquivo_json)

print("Dados salvos no arquivo 'message.json'")
