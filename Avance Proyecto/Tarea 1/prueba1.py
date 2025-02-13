import psutil
import subprocess
import os
import signal
import time

def listar_procesos():
    """Lista los procesos activos en el sistema."""
    print("\nID\tNombre")
    print("-" * 30)
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            print(f"{proc.info['pid']}\t{proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def iniciar_proceso(comando):
    """Inicia un proceso dado un comando."""
    try:
        proceso = subprocess.Popen(comando, shell=True, preexec_fn=os.setsid)
        print(f"Proceso iniciado con PID: {proceso.pid}")
        return proceso.pid
    except Exception as e:
        print(f"Error al iniciar el proceso: {e}")

def detener_proceso(pid):
    """Detiene un proceso dado su PID."""
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Proceso {pid} detenido correctamente.")
    except ProcessLookupError:
        print("Error: No se encontró el proceso.")
    except PermissionError:
        print("Error: Permiso denegado.")

def monitorear_recursos(pid):
    """Monitorea el uso de CPU y memoria de un proceso."""
    try:
        proceso = psutil.Process(pid)
        while True:
            uso_cpu = proceso.cpu_percent(interval=1)
            uso_memoria = proceso.memory_info().rss / (1024 * 1024)  # Convertir a MB
            print(f"PID: {pid} - CPU: {uso_cpu}% - Memoria: {uso_memoria:.2f} MB")
            time.sleep(2)
    except psutil.NoSuchProcess:
        print("El proceso ha finalizado.")
    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")

if __name__ == "__main__":
    while True:
        print("\n--- Gestor de Procesos ---")
        print("1. Listar procesos")
        print("2. Iniciar proceso")
        print("3. Detener proceso")
        print("4. Monitorear proceso")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            listar_procesos()
        elif opcion == "2":
            comando = input("Ingrese el comando a ejecutar: ")
            iniciar_proceso(comando)
        elif opcion == "3":
            pid = int(input("Ingrese el PID del proceso a detener: "))
            detener_proceso(pid)
        elif opcion == "4":
            pid = int(input("Ingrese el PID del proceso a monitorear: "))
            monitorear_recursos(pid)
        elif opcion == "5":
            print("Saliendo del gestor de procesos...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
