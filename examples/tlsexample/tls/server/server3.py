from flask import Flask, request
import ssl
from OpenSSL import crypto

app = Flask(__name__)

# Configurações do servidor Flask
HOST = 'localhost'
PORT = 12345

@app.route('/mensagem', methods=['POST'])
def receive_message():
    try:
        # Obtém o certificado do cliente
        cert = request.environ.get('SSL_CLIENT_CERT')

        if cert:
            # Decodifica o certificado e obtém informações, se necessário
            certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            subject = certificate.get_subject()
            common_name = subject.commonName
            print(f'Common Name do Cliente: {common_name}')

            # Autenticação do cliente - adicione sua lógica de autenticação aqui
            if common_name == 'NomeComumEsperado':
                message = request.data.decode('utf-8')
                print(f'Mensagem recebida: {message}')
                response_message = "Servidor Flask responde: Mensagem recebida com sucesso!"
                return response_message, 200
            else:
                return "Autenticação do cliente falhou", 403
        else:
            return "Certificado do cliente não fornecido", 403

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Configurações de TLS/SSL
    SSL_CERTIFICATE = 'server-cert.pem'
    SSL_KEY = 'server-key.pem'

    # Carrega os certificados SSL/TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_KEY)

    # Configura a verificação do certificado do cliente
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_verify_locations(cafile='ca-cert.pem')  # O certificado CA usado para verificar o cliente

    # Inicia o servidor Flask com TLS/SSL
    app.run(host=HOST, port=PORT, ssl_context=context)
