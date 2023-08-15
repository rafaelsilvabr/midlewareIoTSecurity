import json
from ecdhe_middleware import ECDHEMiddleware
from aes_middleware import AESMiddleware
from tls_ssl_middleware import TLSSSLMiddleware
from token_middleware import TokenMiddleware
from api_keys_middleware import APIKeysMiddleware

class CentralMiddleware:
    def __init__(self, device_id, protocol):
        self.device_id = device_id
        self.protocol = protocol

        # Carregar as configurações do dispositivo a partir de um arquivo
        self.load_device_config()

        # Configurar middleware específico com base no protocolo
        if self.protocol == "ECDHE":
            self.middleware = ECDHEMiddleware(self.device_config)
        elif self.protocol == "AES":
            self.middleware = AESMiddleware(self.device_config)
        elif self.protocol == "TLS/SSL":
            self.middleware = TLSSSLMiddleware(self.device_config)
        elif self.protocol == "Token":
            self.middleware = TokenMiddleware(self.device_config)
        elif self.protocol == "API Keys":
            self.middleware = APIKeysMiddleware(self.device_config)
        else:
            raise ValueError("Protocol not supported")

    def load_device_config(self):
        with open(f"{self.device_id}_config.json", "r") as config_file:
            self.device_config = json.load(config_file)

    def handle_request(self, encrypted_data):
        decrypted_data = self.middleware.decrypt_data(encrypted_data)
        # Processar os dados descriptografados
        pass

# Uso do middleware central
if __name__ == "__main__":
    device_id = "device1"
    protocol = "ECDHE"  # Pode ser "ECDHE", "AES", "TLS/SSL", "Token" ou "API Keys"

    central_middleware = CentralMiddleware(device_id, protocol)
    encrypted_data = b"..."  # Simulação de dados criptografados recebidos
    central_middleware.handle_request(encrypted_data)
