from flask import Blueprint, jsonify

from datetime import datetime

# Creamos el Blueprint:
# - 'health': Nombre identificador interno en Flask
# - __name__: Módulo de origen para resolución de recursos
# - url_prefix: Prefijo común para todas las rutas de este Blueprint
health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route("", methods=["GET"])
def health_check():
    """
    Función que responde a las peticiones GET en la ruta /health.
    Retorna un objeto JSON con el estado del servicio.
    URL accesible: GET /health
    """
    return jsonify({
        "status": "ok",
        "msg": "Servidor Python para API usando Flask, funcionando correctamente!",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200
