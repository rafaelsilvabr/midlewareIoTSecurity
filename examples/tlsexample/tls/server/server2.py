from flask import Flask, request

import ssl

app = Flask(__name__)

# Configurações do servidor Flask
HOST = 'localhost'
PORT = 12345

# Configurações de TLS/SSL
SSL_CERTIFICATE = 'server-cert.pem'
SSL_KEY = 'server-key.pem'

# Dicionário para armazenar dados do cliente autenticado
client_data = {}

@app.route('/mensagem', methods=['POST'])
def receive_message():
    try:
        # Verifica se o cliente forneceu um certificado
        client_cert = request.environ.get('SSL_CLIENT_CERT')

        if client_cert:
            # O cliente forneceu um certificado válido
            client_data['client_certificate'] = client_cert.decode('utf-8')

            message = request.data.decode('utf-8')
            print(f'Mensagem recebida: {message}')

            # Responde à mensagem
            response_message = "Servidor Flask responde: Mensagem recebida com sucesso!"
            return response_message, 200
        else:
            return "Erro de autenticação do cliente", 403

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Carrega os certificados SSL/TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_KEY)

    # Inicia o servidor Flask com TLS/SSL
    app.run(host=HOST, port=PORT, ssl_context=context)
