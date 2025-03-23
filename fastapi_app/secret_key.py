import secrets

secret_key = secrets.token_hex(32)  # Generates a 32-byte hex string
print(secret_key)
