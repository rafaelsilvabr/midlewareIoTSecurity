from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

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
message = b"hello world"

# Configurar o padding para a mensagem
padder = padding.PKCS7(algorithms.AES.block_size).padder()
padded_message = padder.update(message) + padder.finalize()

# Usar AES para encriptar a mensagem
cipher = Cipher(algorithms.AES(key), modes.ECB())  # Modo ECB para fins de exemplo
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_message) + encryptor.finalize()

print("Mensagem encriptada:", ciphertext)

# Desencriptar a mensagem
decryptor = cipher.decryptor()
decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

# Remover o padding
unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

print("Mensagem desencriptada:", decrypted_message)
