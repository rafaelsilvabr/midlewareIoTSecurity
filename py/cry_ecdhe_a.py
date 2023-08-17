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

salt = b"some_salt"  # O salt usado para derivação de chave
iterations = 100000  # Número de iterações do PBKDF2

# Derivar chave de criptografia da chave secreta compartilhada
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # Tamanho da chave AES em bytes
    salt=salt,
    iterations=iterations
)
shared_key_a = base64.b64decode(keys["shared_key"])
encryption_key = kdf.derive(shared_key_a)

# Mensagem a ser criptografada
message = b"Boa tarde!"

# Configurar o padding para a mensagem
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_message = padder.update(message) + padder.finalize()

# Usar AES para encriptar a mensagem
cipher = Cipher(algorithms.AES(encryption_key), modes.ECB()) 
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_message) + encryptor.finalize()

# Serializar a mensagem encriptada e outros parâmetros relevantes
encrypted_data = {
    "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    "salt": base64.b64encode(salt).decode("utf-8"),
    "iterations": iterations
}

# Salvar os dados no arquivo JSON
with open("message_ecdhe.json", "w") as arquivo_json:
    json.dump(encrypted_data, arquivo_json)

print("Mensagem Criptografada enviada")
