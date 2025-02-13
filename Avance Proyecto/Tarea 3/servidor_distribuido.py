import socket
import psutil
import subprocess
import os
import signal

HOST = '0.0.0.0'
PUERTO = 6000  # Puerto del servidor
MIDDLEWARE_IP = '127.0.0.1'  # Dirección del middleware
MIDDLEWARE_PUERTO = 5000  # Puerto del middleware

def registrar_en_middleware():
    """ Registra este servidor en el middleware. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((MIDDLEWARE_IP, MIDDLEWARE_PUERTO))
            mensaje = f"registrar {HOST} {PUERTO}"
            sock.sendall(mensaje.encode())
        except:
            print("Error al conectar con el middleware.")

def listar_procesos():
    procesos = [f"{proc.pid} - {proc.name()}" for proc in psutil.process_iter(attrs=['pid', 'name'])]
    return "\n".join(procesos)

def iniciar_proceso(comando):
    try:
        proceso = subprocess.Popen(comando, shell=True, preexec_fn=os.setsid)
        return f"Proceso iniciado con PID: {proceso.pid}"
    except Exception as e:
        return f"Error al iniciar el proceso: {e}"

def detener_proceso(pid):
    try:
        os.kill(int(pid), signal.SIGTERM)
        return f"Proceso {pid} detenido correctamente."
    except:
        return "Error al detener el proceso."

def manejar_cliente(conexion):
    while True:
        try:
            mensaje = conexion.recv(1024).decode()
            if not mensaje:
                break

            comando = mensaje.split(" ", 1)
            accion = comando[0].lower()

            if accion == "listar":
                respuesta = listar_procesos()
            elif accion == "iniciar" and len(comando) > 1:
                respuesta = iniciar_proceso(comando[1])
            elif accion == "detener" and len(comando) > 1:
                respuesta = detener_proceso(comando[1])
            else:
                respuesta = "Comando no reconocido."

            conexion.sendall(respuesta.encode())
        except:
            break

    conexion.close()

def iniciar_servidor():
    registrar_en_middleware()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PUERTO))
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PUERTO}")

        while True:
            conexion, direccion = servidor.accept()
            manejar_cliente(conexion)

if __name__ == "__main__":
    iniciar_servidor()
