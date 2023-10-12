from flask import Flask, request

import ssl

app = Flask(__name__)

# Configurações do servidor Flask
HOST = 'localhost'
PORT = 12345

# Configurações de TLS/SSL
SSL_CERTIFICATE = 'server-cert.pem'
SSL_KEY = 'server-key.pem'

@app.route('/mensagem', methods=['POST'])
def receive_message():
    try:
        message = request.data.decode('utf-8')
        print(f'Mensagem recebida: {message}')

        # Responde à mensagem
        response_message = "Servidor Flask responde: Mensagem recebida com sucesso!"
        return response_message, 200

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Carrega os certificados SSL/TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_KEY)

    # Inicia o servidor Flask com TLS/SSL
    app.run(host=HOST, port=PORT, ssl_context=context)
