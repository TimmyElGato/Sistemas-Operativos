import socket
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Clave de cifrado
PASSWORD = "sistemas_operativos_rules_2025"

def derive_key(password):
    """Genera una clave de 32 bytes a partir de la contraseña"""
    return hashlib.sha256(password.encode()).digest()

def decrypt_message(encrypted_data, key):
    """Desencripta el mensaje usando AES-CBC"""
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]  # Extrae el IV de los primeros 16 bytes
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_padded.rstrip(b"\0").decode()  # Elimina padding

def start_server():
    """Inicia el servidor en AWS para recibir mensajes cifrados"""
    key = derive_key(PASSWORD)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))  # Escucha en el puerto 12345
    server_socket.listen(1)

    print("Servidor esperando conexiones en el puerto 12345...")

    conn, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")

    encrypted_data = conn.recv(1024).decode()
    decrypted_message = decrypt_message(encrypted_data, key)

    print(f"Mensaje recibido: {decrypted_message}")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
