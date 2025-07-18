import os
from cryptography.fernet import Fernet

KEY_FILE = 'data/.fernet.key'

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return Fernet(key)

fernet = load_key()

def encrypt_msg(message: str) -> str:
    return fernet.encrypt(message.encode()).decode()

def decrypt_msg(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
