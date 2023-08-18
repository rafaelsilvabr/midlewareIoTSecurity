from kafka import KafkaProducer

class KafkaSender:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol="SSL",  # Use "SSL" se necessário
            ssl_cafile="kafka/ca.crt",  # Caminho para o arquivo de certificado CA
            ssl_certfile="kafka/client.crt",  # Caminho para o arquivo de certificado do cliente
            ssl_keyfile="kafka/client.key",  # Caminho para o arquivo de chave do cliente
        )

    def send_message(self, topic, message):
        try:
            self.producer.send(topic, message.encode())
            print("Mensagem enviada com sucesso para o tópico:", topic)
        except Exception as e:
            print("Erro ao enviar mensagem:", str(e))

# Exemplo de uso
if __name__ == "__main__":
    kafka_sender = KafkaSender(bootstrap_servers="server")
    kafka_topic = "topic"
    message = "Hello, Kafka!"
    kafka_sender.send_message(kafka_topic, message)
