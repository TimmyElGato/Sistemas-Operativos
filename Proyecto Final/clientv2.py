import requests

server_url = "https://IP_PUBLICA_AWS:5000" # Aquí ponemos la IP pública de nuestra instancia

# Paso 1: Obtener el token JWT
login_data = {"username": "admin", "password": "1234"} #Ingresamos el usuario y la contraseña que creamos en el servidor
login_response = requests.post(f"{server_url}/login", json=login_data, verify=False)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print("Autenticación exitosa. Token obtenido.")

    # Paso 2: Hacer la solicitud autenticada
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{server_url}/procesos", headers=headers, verify=False)

    if response.status_code == 200:
        print("Procesos en AWS:\n", response.json()["procesos"])
    else:
        print("Error al obtener procesos:", response.text)
else:
    print("Error de autenticación:", login_response.text)
