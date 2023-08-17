from cryptography.fernet import Fernet

# Gere uma chave de criptografia
key = Fernet.generate_key()

# Crie um objeto Fernet usando a chave
fernet = Fernet(key)

# Dado a ser criptografado
data_to_encrypt = b"Hello, world!"

# Criptografe os dados
encrypted_data = fernet.encrypt(data_to_encrypt)

# Descriptografe os dados
decrypted_data = fernet.decrypt(encrypted_data)

print("Dados originais:", data_to_encrypt)
print("Dados criptografados:", encrypted_data)
print("Dados descriptografados:", decrypted_data)