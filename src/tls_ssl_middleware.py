import json
from kafka_ssl_producer import KafkaSSLProducer
import ssl

class TLSSSLMiddleware:
    def __init__(self, private_key_path, cert_path, ca_cert_path):
        self.private_key_path = private_key_path
        self.cert_path = cert_path
        self.ca_cert_path = ca_cert_path

        # Configurar o Kafka SSL Producer
        self.kafka_producer = KafkaSSLProducer(
            bootstrap_servers='localhost:9093',
            ssl_cafile=self.ca_cert_path,
            ssl_certfile=self.cert_path,
            ssl_keyfile=self.private_key_path
        )

    def encrypt_and_send(self, device_public_key, message):
        message_to_send = {
            "message": message
        }
        self.kafka_producer.send_message('device_messages', device_public_key.hex(), json.dumps(message_to_send))

    def decrypt_message(self, encrypted_message):
        return encrypted_message['message']

    def process_encrypted_message(self, encrypted_message):
        decrypted_message = self.decrypt_message(json.loads(encrypted_message))
        print(f"Received decrypted message: {decrypted_message}")

if __name__ == "__main__":
    private_key_path = 'path/to/private.key'
    cert_path = 'path/to/cert.crt'
    ca_cert_path = 'path/to/ca.crt'

    tls_ssl_middleware = TLSSSLMiddleware(private_key_path, cert_path, ca_cert_path)

    # Exemplo de chave pública do dispositivo IoT
    device_public_key = bytes.fromhex("device_public_key_here")

    # Exemplo de mensagem a ser encriptada e enviada para o dispositivo IoT
    message_to_send = "Hello from middleware"
    tls_ssl_middleware.encrypt_and_send(device_public_key, message_to_send)

    # Exemplo de mensagem recebida do dispositivo IoT
    received_message = '{"message": "encrypted_message_here"}'
    tls_ssl_middleware.process_encrypted_message(received_message)
