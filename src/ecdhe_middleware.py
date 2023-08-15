import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from kafka_ssl_producer import KafkaSSLProducer

class ECDHEMiddleware:
    def __init__(self, private_key_data):
        self.private_key_data = private_key_data

        # Configurar o Kafka SSL Producer
        self.kafka_producer = KafkaSSLProducer(
            bootstrap_servers='localhost:9093',
            ssl_cafile='path/to/ca.crt',
            ssl_certfile='path/to/client.crt',
            ssl_keyfile='path/to/client.key'
        )

    def decrypt_data(self, encrypted_data):
        private_key = ec.derive_private_key(
            int.from_bytes(self.private_key_data, "big"),
            ec.SECP256R1(),
            default_backend()
        )

        # Decodificar a chave pública efêmera do dispositivo e o IV
        ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), encrypted_data['ephemeral_public_key'])
        iv = encrypted_data['iv']

        # Derivar chave compartilhada
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)

        # Descriptografar mensagem
        cipher = Cipher(algorithms.AES(derived_key), modes.CFB8(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_data['encrypted_message']) + decryptor.finalize()

        return decrypted_message.decode('utf-8')

    def process_encrypted_message(self, encrypted_message):
        decrypted_message = self.decrypt_data(encrypted_message)
        print(f"Received decrypted message: {decrypted_message}")
        #Enviar dado ao Kafka

if __name__ == "__main__":
    # Carregar chave privada do middleware
    private_key_data = bytes.fromhex("private_key_here")

    ecdhe_middleware = ECDHEMiddleware(private_key_data)

    # Exemplo de mensagem encriptada recebida do dispositivo IoT
    encrypted_message = {
        "ephemeral_public_key": bytes.fromhex("device_ephemeral_public_key_here"),
        "iv": bytes.fromhex("iv_here"),
        "encrypted_message": bytes.fromhex("encrypted_message_here")
    }

    ecdhe_middleware.process_encrypted_message(encrypted_message)
