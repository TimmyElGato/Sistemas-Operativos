from flask import Flask, request
import ssl

app = Flask(__name__)

@app.route('/procesos', methods=['GET'])
def listar_procesos():
    import os
    procesos = os.popen("ps aux").read()
    return f"<pre>{procesos}</pre>"

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')  # Se generan estos archivos antes de correr por primera vez el programa
    app.run(host='0.0.0.0', port=5000, ssl_context=context)
