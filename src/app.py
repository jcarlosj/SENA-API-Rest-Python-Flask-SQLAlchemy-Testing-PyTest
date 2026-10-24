from flask import Flask, jsonify
from typing import Any, Dict, Optional
from src.routes.health import health_bp       # Importamos el Blueprint del módulo health
from datetime import datetime


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:  
    """Application Factory (create_app): Refactorizado app.py con inyección de configuración dinámica (test_config)."""

    # Inicializamos la aplicación Flask
    app = Flask(__name__)

    # 1. Configuración base por defecto (valores de fábrica)
    app.config.from_mapping(
        SECRET_KEY="dev_key_para_desarrollo_local",
    )

    # 2. Reemplazo opcional para pruebas
    if test_config is not None:
        app.config.update(test_config)

    # Registro de rutas / endpoints (módulos tematicos, Blueprints)
    app.register_blueprint(health_bp)             # Registramos el Blueprint en la aplicación

    return app

# Arrancamos la aplicación: Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    app = create_app()                              # Crear la instancia de la aplicación (sin config de prueba)
    app.run(debug=True, port=5000, host='0.0.0.0')  # Ejecutamos la aplicación en modo debug

    # kill -9 $(lsof -t -i:5000)   
    # python src/app.py o python -m src.app


