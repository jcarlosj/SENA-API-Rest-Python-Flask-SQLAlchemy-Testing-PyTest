from flask import Flask, jsonify
from datetime import datetime

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Definimos la ruta /health
@app.route('/health', methods=['GET'])
def health_check():
    """
    Función que responde a las peticiones GET en la ruta /health.
    Retorna un objeto JSON con el estado del servicio.
    """
    return jsonify({
        "status": "ok",
        "service": "Servidor Python para API usando Flask, funcionando correctamente!",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200

# Arrancamos la aplicación: Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')