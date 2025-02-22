import socket
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Contraseña utilizada para el cifrado (debe ser de 32 bytes para AES-256)
PASSWORD = b"sistemas_operativos_rules_2025".ljust(32, b"0")  # Se ajusta a 32 bytes

def decrypt_message(encrypted_message, nonce):
    """Función para descifrar un mensaje usando AES-GCM"""
    cipher = Cipher(algorithms.AES(PASSWORD), modes.GCM(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    return decrypted_message.decode()

def start_server():
    """Función que inicializa el servidor y recibe mensajes cifrados"""
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print("Esperando conexión del cliente...")
    conn, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")

    # Recibir datos
    data = conn.recv(1024)
    nonce, encrypted_message = data.split(b"||")  # Separar nonce del mensaje cifrado

    # Descifrar mensaje
    try:
        decrypted_message = decrypt_message(encrypted_message, nonce)
        print(f"Mensaje recibido y descifrado: {decrypted_message}")
    except Exception as e:
        print(f"Error al descifrar el mensaje: {e}")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
