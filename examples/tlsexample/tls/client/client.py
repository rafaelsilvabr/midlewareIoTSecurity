import requests

# Configurações do servidor Flask
SERVER_URL = 'https://localhost:12345/mensagem'  # URL do servidor com o endpoint correto

# Configurações do certificado do cliente (opcional)
CLIENT_CERTIFICATE = 'client-cert.pem'
CLIENT_KEY = 'client-key.pem'

# Define uma função para enviar uma mensagem para o servidor
def send_message(message):
    try:
        # Cria um dicionário com os dados da mensagem
        data = {'message': message}

        # Configura o certificado do cliente
        client_cert = (CLIENT_CERTIFICATE, CLIENT_KEY)

        # Faz a solicitação POST ao servidor usando TLS/SSL com certificado de cliente
        response = requests.post(SERVER_URL, json=data, cert=client_cert, verify=False)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            print(f'Resposta do servidor: {response.text}')
        else:
            print(f'Erro na solicitação. Código de status: {response.status_code}')

    except requests.exceptions.SSLError as e:
        print(f'Erro SSL: {e}')

if __name__ == '__main__':
    message_to_send = "Esta é uma mensagem de teste."

    # Envia a mensagem para o servidor
    send_message(message_to_send)
