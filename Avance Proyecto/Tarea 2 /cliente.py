import socket

HOST = '127.0.0.1'  # Dirección IP del servidor (ajustar si es necesario)
PUERTO = 65432      # Puerto del servidor

def enviar_comando(comando):
    """ Envía un comando al servidor y recibe la respuesta. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PUERTO))
            cliente.sendall(comando.encode())
            respuesta = cliente.recv(4096).decode()
            print(f"Respuesta del servidor:\n{respuesta}")
        except ConnectionRefusedError:
            print("Error: No se pudo conectar al servidor.")

if __name__ == "__main__":
    while True:
        print("\n--- Cliente de Gestión de Procesos ---")
        print("1. Listar procesos")
        print("2. Iniciar proceso")
        print("3. Detener proceso")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            enviar_comando("listar")
        elif opcion == "2":
            comando = input("Ingrese el comando a ejecutar: ")
            enviar_comando(f"iniciar {comando}")
        elif opcion == "3":
            pid = input("Ingrese el PID del proceso a detener: ")
            enviar_comando(f"detener {pid}")
        elif opcion == "4":
            enviar_comando("salir")
            print("Saliendo del cliente...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
