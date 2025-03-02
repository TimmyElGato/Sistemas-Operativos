import socket
import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Clave de cifrado
PASSWORD = "sistemas_operativos_rules_2025"

def derive_key(password):
    """Genera una clave de 32 bytes a partir de la contraseña"""
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(message, key):
    """Encripta el mensaje usando AES-CBC"""
    iv = os.urandom(16)  # IV aleatorio de 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding para que el mensaje sea múltiplo de 16 bytes
    padded_message = message.ljust(16 * ((len(message) // 16) + 1), "\0").encode()

    encrypted_data = encryptor.update(padded_message) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode()  # En Base64 para enviar por red

def send_message(message, server_ip):
    """Conecta al servidor en AWS y envía el mensaje cifrado"""
    key = derive_key(PASSWORD)
    encrypted_message = encrypt_message(message, key)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))  # Conectar con el servidor AWS

    client_socket.send(encrypted_message.encode())  # Enviar mensaje cifrado
    print(f"Mensaje enviado: {encrypted_message}")

    client_socket.close()

if __name__ == "__main__":
    mensaje = input("Escribe tu mensaje: ")
    send_message(mensaje, "IP_PUBLICA_AWS")
