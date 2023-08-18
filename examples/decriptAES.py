from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def decrypt_AES(encrypted_message, key):
    backend = default_backend()

    # Decodificar a mensagem encriptada de base64
    encrypted_bytes = base64.b64decode(encrypted_message)

    # Extrair o IV (primeiros 16 bytes)
    iv = encrypted_bytes[:16]

    # Resto dos bytes são o texto cifrado
    ciphertext = encrypted_bytes[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    # Decifrar o texto cifrado
    decrypted_padded_message = decryptor.update(ciphertext) + decryptor.finalize()

    # Remover o padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message_bytes = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    # Decodificar os bytes da mensagem para string
    decrypted_message = decrypted_message_bytes.decode("utf-8")

    return decrypted_message

# Chave AES em formato Base64URL (44 caracteres)
base64_url_key = "aRnEFjIiYerS3FOFIUn-kHbHAy-vUfXIDlMXJUg54V4="
key_bytes = base64.urlsafe_b64decode(base64_url_key)  # Decodifica Base64URL para bytes

# Mensagem encriptada (de exemplo)
base64_encrypted_message = "7362mWHYnbFO2Cgm1ZwEUrsAEaQeMl+HfJbdd08xNouVV0kMkbnc7kGu49afc6BJ"  # Coloque a mensagem encriptada aqui

# Decriptar a mensagem
decrypted_message = decrypt_AES(base64_encrypted_message, key_bytes)

print("Mensagem decriptada:", decrypted_message)
