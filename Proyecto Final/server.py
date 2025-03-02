import requests

server_url = "https://3.80.204.168:5000" #IP Pública del servidor

# Paso 1: Obtener el token JWT
login_data = {"username": "admin", "password": "1234"}
login_response = requests.post(f"{server_url}/login", json=login_data, verify=False)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print("Autenticación exitosa. Token obtenido.")

    headers = {"Authorization": f"Bearer {token}"}

    while True:
        print("\nOpciones:")
        print("1. Ver procesos")
        print("2. Detener un proceso")
        print("3. Iniciar un proceso")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            response = requests.get(f"{server_url}/procesos", headers=headers, verify=False)
            if response.status_code == 200:
                print("Procesos en AWS:\n", response.json()["procesos"])
            else:
                print("Error al obtener procesos:", response.text)

        elif opcion == "2":
            pid = input("Introduce el PID del proceso a detener: ")
            response = requests.post(f"{server_url}/detener_proceso", json={"pid": pid}, headers=headers, verify=False)
            print(response.json())

        elif opcion == "3":
            comando = input("Introduce el comando para iniciar el proceso: ")
            response = requests.post(f"{server_url}/iniciar_proceso", json={"comando": comando}, headers=headers, verify=False)
            print(response.json())

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

else:
    print("Error de autenticación:", login_response.text)
