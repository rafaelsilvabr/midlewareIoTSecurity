import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend  # Importe o backend

# Gere uma chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()  # Use o backend
)

# Crie um certificado autoassinado
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Goias"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Goiania"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UFG"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    # This cert will be valid for 10 days
    datetime.datetime.utcnow() + datetime.timedelta(days=10)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())  # Especifique o backend aqui

# Salve a chave privada e o certificado em arquivos PEM
with open("client/client-key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

with open("client/client-cert.pem", "wb") as f:
    f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))
