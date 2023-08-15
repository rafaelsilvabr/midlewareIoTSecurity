from kafka import KafkaProducer
import ssl

class KafkaSSLProducer:
    def __init__(self, bootstrap_servers, ssl_cafile, ssl_certfile, ssl_keyfile):
        self.bootstrap_servers = bootstrap_servers
        self.ssl_cafile = ssl_cafile
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile

        self.producer = self._create_producer()

    def _create_producer(self):
        ssl_context = ssl.create_default_context(
            cafile=self.ssl_cafile,
            certfile=self.ssl_certfile,
            keyfile=self.ssl_keyfile
        )
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            security_protocol="SSL",
            ssl_context=ssl_context
        )

    def send_message(self, topic, message_key, message_value):
        self.producer.send(topic, key=message_key.encode('utf-8'), value=message_value.encode('utf-8'))
        self.producer.flush()
