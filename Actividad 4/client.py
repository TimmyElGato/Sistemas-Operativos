import socket
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Contraseña utilizada para el cifrado (debe ser de 32 bytes para AES-256)
PASSWORD = b"sistemas_operativos_rules_2025".ljust(32, b"0")  # Se ajusta a 32 bytes

def encrypt_message(message):
    """Función para cifrar un mensaje usando AES-GCM"""
    nonce = os.urandom(12)  # Generar un nonce de 12 bytes (recomendado para GCM)
    cipher = Cipher(algorithms.AES(PASSWORD), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    return nonce, encrypted_message

def send_message():
    """Función para enviar un mensaje cifrado al servidor"""
    host = "127.0.0.1"
    port = 12345

    # Mensaje a enviar
    message = input("Escribe el mensaje a enviar: ")

    # Cifrar mensaje
    nonce, encrypted_message = encrypt_message(message)

    # Conectar al servidor y enviar datos
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Enviar nonce y mensaje cifrado, separados por "||"
    client_socket.sendall(nonce + b"||" + encrypted_message)
    
    print("Mensaje cifrado enviado correctamente.")
    client_socket.close()

if __name__ == "__main__":
    send_message()
