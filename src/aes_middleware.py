import json
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from kafka_ssl_producer import KafkaSSLProducer

class AESMiddleware:
    def __init__(self, private_key_data, device_public_key_data):
        self.private_key_data = private_key_data
        self.device_public_key_data = device_public_key_data

        # Configurar o Kafka SSL Producer
        self.kafka_producer = KafkaSSLProducer(
            bootstrap_servers='localhost:9093',
            ssl_cafile='path/to/ca.crt',
            ssl_certfile='path/to/client.crt',
            ssl_keyfile='path/to/client.key'
        )

    def encrypt_data(self, message):
        private_key = self.private_key_data
        device_public_key = self.device_public_key_data

        # Derivar chave compartilhada usando a chave privada e pública
        shared_key = private_key + device_public_key
        derived_key = shared_key[:32]  # Usar os primeiros 32 bytes para a chave do AES

        # Criptografar mensagem
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(derived_key), modes.CFB8(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(message.encode('utf-8')) + encryptor.finalize()

        return iv + encrypted_message

    def decrypt_data(self, encrypted_data):
        private_key = self.private_key_data
        device_public_key = self.device_public_key_data

        # Derivar chave compartilhada usando a chave privada e pública
        shared_key = private_key + device_public_key
        derived_key = shared_key[:32]  # Usar os primeiros 32 bytes para a chave do AES

        # Decodificar IV e mensagem criptografada
        iv = encrypted_data[:16]
        encrypted_message = encrypted_data[16:]

        # Descriptografar mensagem
        cipher = Cipher(algorithms.AES(derived_key), modes.CFB8(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        return decrypted_message.decode('utf-8')

    def encrypt_and_send(self, message):
        encrypted_message = self.encrypt_data(message)
        self.kafka_producer.send_message('device_messages', self.device_public_key_data.hex(), encrypted_message.hex())

    def process_encrypted_message(self, encrypted_message):
        decrypted_message = self.decrypt_data(bytes.fromhex(encrypted_message))
        print(f"Received decrypted message: {decrypted_message}")

if __name__ == "__main__":
    # Carregar chave privada do middleware e chave pública do dispositivo
    private_key_data = bytes.fromhex("private_key_here")
    device_public_key_data = bytes.fromhex("device_public_key_here")

    aes_middleware = AESMiddleware(private_key_data, device_public_key_data)

    # Exemplo de mensagem a ser encriptada e enviada para o dispositivo IoT
    message_to_send = "Hello from middleware"
    aes_middleware.encrypt_and_send(message_to_send)

    # Exemplo de mensagem encriptada recebida do dispositivo IoT
    encrypted_message = "encrypted_message_here"
    aes_middleware.process_encrypted_message(encrypted_message)
