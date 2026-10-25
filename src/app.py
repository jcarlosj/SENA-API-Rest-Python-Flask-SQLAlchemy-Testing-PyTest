from src.routes.users_routes import users_bp
from flask import Flask, jsonify
from typing import Any, Dict, Optional

from datetime import datetime

from src.routes.health import health_bp       # Importamos el Blueprint del módulo health
from src.config.mysql_config import Config, verify_database_connection
from src.models import db                     # Importamos db de SQLAlchemy

def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:  
    """Application Factory (create_app): Refactorizado app.py con inyección de configuración dinámica (test_config)."""

    # 0. Inicializamos la aplicación Flask
    app = Flask(__name__)

    # 1. Carga configuración base de datos Config (Incluye la URI de MySQL)
    app.config.from_object(Config)

    # 1. Configuración base por defecto (valores de fábrica)
    # app.config.from_mapping(
    #     SECRET_KEY="dev_key_para_desarrollo_local",
    # )

    # 2. Reemplazo opcional para pruebas
    if test_config is not None:
        app.config.update(test_config)

    # 3. Inicializamos la base de datos con la aplicación Flask
    db.init_app(app)

    # 4. Registro de rutas / endpoints (módulos tematicos, Blueprints)
    app.register_blueprint(health_bp)                               # Registramos el Blueprint en la aplicación
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')    # Registramos el Blueprint en la aplicación

    return app

# Arrancamos la aplicación: Punto de entrada para ejecutar el servidor
if __name__ == '__main__':
    # Verificamos la conexión a la base de datos antes de iniciar el servidor
    verify_database_connection(Config.SQLALCHEMY_DATABASE_URI)

    # Crear la instancia de la aplicación (sin config de prueba)
    app = create_app()                              

    # Crea automáticamente las tablas en MySQL si aún no existen
    with app.app_context():
        db.create_all()                             # Crea todas las tablas definidas en los modelos

    # Ejecutamos la aplicación en modo debug
    app.run(debug=True, port=5000, host='0.0.0.0')  

    # Comandos a ejecutar

    # python src/app.py                                 Ejecuta la aplicacion
    # python -m src.app                                 Ejecuta la aplicacion
    # kill -9 $(lsof -t -i:5000)                        Detiene la aplicacion si está en uso

    # pip install SQLAlchemy pymysql cryptography pytest pytest-cov

    # pip3 install -r requirements.txt                  Instala las dependencias del proyecto
    # pip3 freeze > requirements.txt                     Actualiza el archivo requirements.txt con las dependencias instaladas
    
    # python -m flask run                               Ejecuta la aplicacion
    # flask --app src.app run --debug                   Ejecuta la aplicacion en modo debug
    # flask --app src.app run --host=[IP_ADDRESS] --port=5000    Ejecuta la aplicacion en modo debug

    # pytest --cov=src --cov-report=term-missing        Ejecuta las pruebas con cobertura
    # pytest --cov=src --cov-report=html                Ejecuta las pruebas con cobertura y genera un reporte HTML
    # La cobertura de código es una métrica porcentual que indica qué proporción de tus líneas de código fuente fueron efectivamente ejecutadas cuando corriste tu suite de pruebas automáticas.

    # pytest --cov=src --cov-report=term-missing --cov-report=html
    # Ejecuta las pruebas con cobertura y genera un reporte HTML.
    # El reporte HTML se puede encontrar en la carpeta htmlcov

    # En Linux: 
    # "xdg-open htmlcov/index.html" o simplemente arrastra el archivo index.html a una pestaña de tu navegador


