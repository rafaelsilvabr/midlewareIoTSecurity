import json
#from kafka_ssl_producer import KafkaSSLProducer

class TokenMiddleware:
    def __init__(self, token_secret):
        self.token_secret = token_secret

        # Configurar o Kafka SSL Producer
        self.kafka_producer = KafkaSSLProducer(
            bootstrap_servers='localhost:9093',
            ssl_cafile='path/to/ca.crt',
            ssl_certfile='path/to/client.crt',
            ssl_keyfile='path/to/client.key'
        )

    def generate_token(self, device_id):
        payload = {'device_id': device_id}
        token = jwt.encode(payload, self.token_secret, algorithm='HS256')
        return token

    def encrypt_and_send(self, device_id, message):
        token = self.generate_token(device_id)
        message_to_send = {
            "message": message,
            "token": token
        }
        self.kafka_producer.send_message('device_messages', device_id, json.dumps(message_to_send))

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.token_secret, algorithms=['HS256'])
            return payload['device_id']
        except jwt.ExpiredSignatureError:
            return None

    def process_encrypted_message(self, encrypted_message):
        token = encrypted_message['token']
        device_id = self.verify_token(token)
        if device_id:
            decrypted_message = encrypted_message['message']
            print(f"Received message from device {device_id}: {decrypted_message}")
        else:
            print("Invalid token received!")

if __name__ == "__main__":
    token_secret = "your_token_secret_here"

    token_middleware = TokenMiddleware(token_secret)

    # Exemplo de mensagem a ser encriptada e enviada para o dispositivo IoT
    device_id = "device1"
    message_to_send = "Hello from middleware"
    token_middleware.encrypt_and_send(device_id, message_to_send)

    # Exemplo de mensagem recebida do dispositivo IoT
    received_message = {
        "message": "encrypted_message_here",
        "token": "valid_token_here"
    }
    token_middleware.process_encrypted_message(received_message)
