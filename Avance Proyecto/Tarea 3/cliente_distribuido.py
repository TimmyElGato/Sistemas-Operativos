import socket

MIDDLEWARE_IP = '127.0.0.1'
MIDDLEWARE_PUERTO = 5000

def obtener_servidores():
    """ Obtiene la lista de servidores disponibles en el middleware. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((MIDDLEWARE_IP, MIDDLEWARE_PUERTO))
        sock.sendall("listar servidores".encode())
        respuesta = sock.recv(4096).decode()
        return respuesta.split("\n") if respuesta else []

def enviar_comando(servidor, comando):
    """ Envía un comando a un servidor específico. """
    ip, puerto = servidor.split(":")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, int(puerto)))
        sock.sendall(comando.encode())
        respuesta = sock.recv(4096).decode()
        print(f"Respuesta del servidor:\n{respuesta}")

if __name__ == "__main__":
    while True:
        print("\n--- Cliente Distribuido ---")
        print("1. Obtener servidores disponibles")
        print("2. Enviar comando a un servidor")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            servidores = obtener_servidores()
            print("Servidores disponibles:")
            for i, srv in enumerate(servidores, 1):
                print(f"{i}. {srv}")
        elif opcion == "2":
            servidores = obtener_servidores()
            if not servidores:
                print("No hay servidores disponibles.")
                continue
            for i, srv in enumerate(servidores, 1):
                print(f"{i}. {srv}")

            seleccion = int(input("Seleccione un servidor: ")) - 1
            if 0 <= seleccion < len(servidores):
                servidor = servidores[seleccion]
                comando = input("Ingrese el comando (listar/iniciar/detener PID): ")
                enviar_comando(servidor, comando)
            else:
                print("Selección inválida.")
        elif opcion == "3":
            print("Saliendo del cliente...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
