from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import os
import ssl
import subprocess

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "clave_super_secreta" 
jwt = JWTManager(app)

# Endpoint para autenticación
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "1234":
        token = create_access_token(identity=data["username"])
        return jsonify(access_token=token)
    return jsonify({"error": "Credenciales incorrectas"}), 401

# Endpoint para obtener la lista de procesos
@app.route('/procesos', methods=['GET'])
@jwt_required()
def listar_procesos():
    procesos = os.popen("ps aux").read()
    return jsonify(procesos=procesos)

# Endpoint para detener un proceso
@app.route('/detener_proceso', methods=['POST'])
@jwt_required()
def detener_proceso():
    data = request.json
    pid = data.get("pid")
    if not pid:
        return jsonify({"error": "Se requiere el PID del proceso"}), 400

    try:
        os.kill(int(pid), 9)  # Señal 9 = SIGKILL
        return jsonify({"mensaje": f"Proceso {pid} detenido exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para iniciar un nuevo proceso
@app.route('/iniciar_proceso', methods=['POST'])
@jwt_required()
def iniciar_proceso():
    data = request.json
    comando = data.get("comando")
    if not comando:
        return jsonify({"error": "Se requiere un comando para ejecutar"}), 400

    try:
        proceso = subprocess.Popen(comando, shell=True)
        return jsonify({"mensaje": f"Proceso iniciado con PID {proceso.pid}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
