import socket
import psutil
import subprocess
import os
import signal

HOST = '0.0.0.0'  # Escucha en todas las interfaces de red
PUERTO = 65432     # Puerto de comunicación

def listar_procesos():
    """ Devuelve una lista de los procesos activos. """
    procesos = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            procesos.append(f"{proc.info['pid']} - {proc.info['name']}")
        except:
            continue
    return "\n".join(procesos)

def iniciar_proceso(comando):
    """ Inicia un nuevo proceso. """
    try:
        proceso = subprocess.Popen(comando, shell=True, preexec_fn=os.setsid)
        return f"Proceso iniciado con PID: {proceso.pid}"
    except Exception as e:
        return f"Error al iniciar el proceso: {e}"

def detener_proceso(pid):
    """ Detiene un proceso por su PID. """
    try:
        os.kill(int(pid), signal.SIGTERM)
        return f"Proceso {pid} detenido correctamente."
    except ProcessLookupError:
        return "Error: No se encontró el proceso."
    except PermissionError:
        return "Error: Permiso denegado."
    except ValueError:
        return "Error: PID inválido."

def manejar_cliente(conexion):
    """ Maneja la comunicación con un cliente. """
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
            elif accion == "salir":
                respuesta = "Desconectando cliente..."
                conexion.sendall(respuesta.encode())
                break
            else:
                respuesta = "Comando no reconocido."

            conexion.sendall(respuesta.encode())
        
        except ConnectionResetError:
            break

    conexion.close()

def iniciar_servidor():
    """ Inicia el servidor y acepta conexiones de clientes. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PUERTO))
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PUERTO}")

        while True:
            conexion, direccion = servidor.accept()
            print(f"Cliente conectado desde {direccion}")
            manejar_cliente(conexion)

if __name__ == "__main__":
    iniciar_servidor()
