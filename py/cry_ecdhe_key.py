from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import json
import base64

# Gerar chaves para as partes A e B
private_key_a = ec.generate_private_key(ec.SECP256R1())  # Ou escolha outra curva adequada
private_key_b = ec.generate_private_key(ec.SECP256R1())

# Obter as chaves públicas
public_key_a = private_key_a.public_key()
public_key_b = private_key_b.public_key()

# Realizar o acordo de chaves
shared_key_a = private_key_a.exchange(ec.ECDH(), public_key_b)
shared_key_b = private_key_b.exchange(ec.ECDH(), public_key_a)

public_key_a_pem = public_key_a.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_key_b_pem = public_key_b.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

shared_key_base64 = base64.b64encode(shared_key_a).decode("utf-8")

keys = {
    "public_key_a": public_key_a_pem.decode("utf-8"),
    "public_key_b": public_key_b_pem.decode("utf-8"),
    "shared_key": shared_key_base64
}

with open("keys.json", "w") as file:
    json.dump(keys, file)

print("Chaves salvas no arquivo 'keys.json'")