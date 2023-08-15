import json
from kafka_ssl_producer import KafkaSSLProducer

class ApiKeysMiddleware:
    def __init__(self, api_keys):
        self.api_keys = api_keys

        # Configurar o Kafka SSL Producer
        self.kafka_producer = KafkaSSLProducer(
            bootstrap_servers='localhost:9093',
            ssl_cafile='path/to/ca.crt',
            ssl_certfile='path/to/client.crt',
            ssl_keyfile='path/to/client.key'
        )

    def decrypt_message(self, encrypted_message, device_key):
        # Simulação de decriptação, substitua por sua lógica real de decriptação
        return f"Decrypted message for device {device_key}: {encrypted_message}"

    def process_encrypted_message(self, encrypted_message):
        device_key = encrypted_message['device_key']
        if device_key in self.api_keys:
            encrypted_data = encrypted_message['message']
            decrypted_message = self.decrypt_message(encrypted_data, device_key)
            print(f"Received and decrypted message from device with API key {device_key}: {decrypted_message}")

            # Enviar mensagem decriptada ao Kafka
            self.kafka_producer.send_message('device_messages', device_key, decrypted_message)
        else:
            print("Invalid API key!")

if __name__ == "__main__":
    api_keys = {
        "api_key1": "device1",
        "api_key2": "device2"
    }

    api_keys_middleware = ApiKeysMiddleware(api_keys)

    # Exemplo de mensagem encriptada recebida do dispositivo IoT
    encrypted_message = {
        "message": "encrypted_message_here",
        "device_key": "api_key1"
    }
    api_keys_middleware.process_encrypted_message(encrypted_message)
