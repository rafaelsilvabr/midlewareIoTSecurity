import json
from flask import Flask, request, jsonify
from ecdhe_middleware import ECDHEMiddleware
from aes_middleware import AESMiddleware
from tls_ssl_middleware import TLSSSLMiddleware
from token_middleware import TokenMiddleware
from api_keys_middleware import ApiKeysMiddleware
import base64

app = Flask(__name__)

import os
import json
from ecdhe_middleware import ECDHEMiddleware
from aes_middleware import AESMiddleware
from tls_ssl_middleware import TLSSSLMiddleware
from token_middleware import TokenMiddleware
from api_keys_middleware import ApiKeysMiddleware
from kafka_producer import KafkaSender

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
            os.remove(f"devices/{data.get('device_id')}_config.json")
            #return json.dumps({"error": f"Device {data.get('device_id')} is already registered.", "device": existing_device})

        device_info = {
            "device_id": data.get("device_id"),
            "kafka_topic": data.get("kafka_topic"),
            "method": data.get("method")
        }

        if data.get("method") == "aes":
            AESdevice = AESMiddleware(data.get("password")) #TODO necessario implementar teste se a password não esta presente
            device_info["key"] = AESdevice.key.decode()
            print(device_info)
        elif data.get("method") == "ecdhe":
            # Ler os dados do arquivo JSON
            AESdevice = AESMiddleware("password") #TODO necessario implementar teste se a password não esta presente
            device_info["key"] = AESdevice.key.decode()
            print(device_info)
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
        print("Device Registrado!")
        return json.dumps({"success": f"Device {data.get('device_id')} registered with {data.get('method')} method.", "device": device_info})

    def handle_event(self, data):
        config_file_path = f"devices/{data.get('device_id')}_config.json"
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as config_file: #TODO implementar try catch
                device_info = json.load(config_file)

            if device_info["method"] == "aes":
                AESdevice = AESMiddleware.from_default()
                AESdevice.key=base64.urlsafe_b64decode(device_info["key"].encode())
                decrypted_data = AESdevice.decrypt(data.get("encrypted_data").encode("utf-8"))  # Substitua pelo método de descriptografia correto da classe AESMiddleware

                print(decrypted_data)

                kafka_sender = KafkaSender("serverhost")
                kafka_topic = data.get("kafka_topic")
                message = decrypted_data
                kafka_sender.send_message(kafka_topic, message)

                return f"Dado do device:{data.get('device_id')} enviado"
            elif device_info["method"] == "ecdhe":
                with open("keys.json", "r") as arquivo_json:
                    keys = json.load(arquivo_json)
                shared_key_a = base64.b64decode(keys["shared_key"])
                encryption_key = kdf.derive(shared_key_a)
                ECDHEdevice = ECDHEMiddleware(shared_key_a)
                print("Debug: Linha 48 Main, teste retorno ECDHEMDW")
                print(ECDHEdevice.key)
                device_info["key"] = ECDHEdevice.key.decode()

                kafka_sender = KafkaSender("serverhost")
                kafka_topic = data.get("kafka_topic")
                message = decrypted_data
                kafka_sender.send_message(kafka_topic, message)

                return f"Dado do device:{data.get('device_id')} enviado"
                # ...

                return f"Received decrypted data from device {device_id}"
            elif device_info["method"] == "tls_ssl":
                # Lógica para TLSSSLMiddleware
                pass
            elif device_info["method"] == "token":
                # Lógica para TokenMiddleware
                pass
            elif device_info["method"] == "api_keys":
                # Lógica para ApiKeysMiddleware
                pass
            else:
                return f"Method {device_info['method']} is not supported."
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
    response = central_middleware.handle_event(data)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
