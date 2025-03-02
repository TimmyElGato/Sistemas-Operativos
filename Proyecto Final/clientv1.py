import requests

url = "https://IP_PUBLICA_AWS:5000/procesos" # Ingresamos la IP Pública de nuestra instancia
response = requests.get(url, verify=False)  # Unicamente se desactiva la verificación para pruebas

print("Procesos en AWS:\n", response.text)
