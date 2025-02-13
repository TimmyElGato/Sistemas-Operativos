import socket
import threading

# Dirección y puerto del middleware
HOST = '0.0.0.0'
PUERTO = 5000

# Lista de servidores registrados
servidores = {}

def manejar_cliente(conexion, direccion):
    """ Maneja solicitudes de clientes y devuelve servidores disponibles. """
    while True:
        try:
            mensaje = conexion.recv(1024).decode()
            if not mensaje:
                break

            if mensaje.lower() == "listar servidores":
                respuesta = "\n".join([f"{ip}:{puerto}" for ip, puerto in servidores.values()])
                if not respuesta:
                    respuesta = "No hay servidores disponibles."
                conexion.sendall(respuesta.encode())

            elif mensaje.startswith("registrar"):
                _, ip, puerto = mensaje.split()
                servidores[direccion] = (ip, int(puerto))
                conexion.sendall(f"Servidor {ip}:{puerto} registrado.".encode())

        except ConnectionResetError:
            break

    conexion.close()

def iniciar_middleware():
    """ Inicia el middleware para conectar clientes con servidores. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PUERTO))
        servidor.listen()
        print(f"Middleware escuchando en {HOST}:{PUERTO}")

        while True:
            conexion, direccion = servidor.accept()
            threading.Thread(target=manejar_cliente, args=(conexion, direccion)).start()

if __name__ == "__main__":
    iniciar_middleware()
