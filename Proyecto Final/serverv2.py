from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import os
import ssl

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "clave_super_secreta"  # Creamos una clave para acceder al servidor
jwt = JWTManager(app)

# Endpoint para autenticación
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "1234":  # Establecemos un usuario y una contraseña
        token = create_access_token(identity=data["username"])
        return jsonify(access_token=token)
    return jsonify({"error": "Credenciales incorrectas"}), 401

# Endpoint protegido con JWT
@app.route('/procesos', methods=['GET'])
@jwt_required()
def listar_procesos():
    procesos = os.popen("ps aux").read()
    return jsonify(procesos=procesos)

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')  # Deberemos crear estos archivos antes de levantar por primera vez el servidor
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
