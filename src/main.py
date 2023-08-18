import json
from flask import Flask, request, jsonify
from ecdhe_middleware import ECDHEMiddleware
from aes_middleware import AESMiddleware
from tls_ssl_middleware import TLSSSLMiddleware
from token_middleware import TokenMiddleware
from api_keys_middleware import ApiKeysMiddleware

app = Flask(__name__)

import os
import json
from ecdhe_middleware import ECDHEMiddleware
from aes_middleware import AESMiddleware
from tls_ssl_middleware import TLSSSLMiddleware
from token_middleware import TokenMiddleware
from api_keys_middleware import ApiKeysMiddleware

class CentralMiddleware:
    def __init__(self):
        self.devices = {}

    def is_device_registered(self, device_id):
        config_file_path = f"devices/{device_id}_config.json"
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as config_file:
                device_info = json.load(config_file)
            return device_info
        return None

    def register_device(self, data):
        #Validar Token Admin
        adm_token = data.get("token")

        #Verificar se o dispositivo já está cadastrado
        existing_device = self.is_device_registered(data.get("device_id"))
        if existing_device:
            return json.dumps({"error": f"Device {data.get('device_id')} is already registered.", "device": existing_device})

        device_info = {
            "device_id": data.get("device_id"),
            "kafka_topic": data.get("kafka_topic"),
            "method": data.get("method")
        }

        if data.get("method") == "aes":
            AESdevice = AESMiddleware(data.get("password")) #TODO necessario implementar teste se a password não esta presente
            print("Debug: Linha 48 Main, teste retorno AESMDW")
            print(AESdevice.key)
            device_info["key"] = AESdevice.key.decode("utf-8")
            print(device_info)
        elif data.get("method") == "ecdhe":
            ECDHEDevice = ECDHEMiddleware()
        elif data.get("method") == "tls_ssl":
            TLSSSLDevice = TLSSSLMiddleware()
        elif data.get("method") == "token":
            TokenDevice = TokenMiddleware()
        elif data.get("method") == "api_keys":
            ApikeysDevice = ApiKeysMiddleware()
        else:
            return json.dumps({"error": f"Method {data.get('method')} is not supported."})

        # Salvar as informações do dispositivo em um arquivo JSON
        with open(f"./devices/{data.get('device_id')}_config.json", "w") as config_file:
            json.dump(device_info, config_file)

        return json.dumps({"success": f"Device {data.get('device_id')} registered with {data.get('method')} method.", "device": device_info})

    def handle_event(self, device_id, encrypted_data):
        if device_id in self.devices:
            decrypted_data = self.devices[device_id].decrypt_data(encrypted_data)
            # Processar os dados descriptografados
            return f"Received decrypted data from device {device_id}: {decrypted_data}"
        else:
            return f"Device {device_id} is not registered."

central_middleware = CentralMiddleware()

@app.route("/register", methods=["POST"])
def register_device():
    data = request.json
    response = central_middleware.register_device(data)
    return jsonify({"response": response})

@app.route("/event", methods=["POST"])
def handle_event():
    data = request.json
    device_id = data.get("device_id")
    encrypted_data = data.get("encrypted_data")
    response = central_middleware.handle_event(device_id, encrypted_data)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
