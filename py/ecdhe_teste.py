from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Gerar um par de chaves ECDHE
private_key = ec.generate_private_key(ec.SECP256R1())  # Curva elíptica P-256
public_key = private_key.public_key()

# Serializar a chave pública para enviar para a outra parte (normalmente, via rede)
serialized_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Suponhamos que a outra parte tenha recebido a chave pública serializada

# Carregar a chave pública da outra parte
received_public_key = serialization.load_pem_public_key(
    serialized_public_key,
    backend=None  # Pode especificar uma implementação específica, como OpenSSL
)

# Fazer a troca de chaves ECDHE
shared_key = private_key.exchange(ec.ECDH(), received_public_key)

print("Chave compartilhada:", shared_key.hex())