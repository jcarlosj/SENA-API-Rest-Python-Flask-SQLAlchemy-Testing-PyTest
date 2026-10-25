import pytest

from sqlalchemy import text
from src.app import create_app
from src.models import db 

"""Pytest reconoce automáticamente un archivo especial llamado tests/conftest.py. Cualquier fixture declarado allí queda disponible para todos los archivos de prueba del proyecto sin necesidad de importarlo manualmente."""

@pytest.fixture
def app():
    # Crea y configura una nueva instancia de la app para cada funcion de test
    test_config = {
        "TESTING": True,                                    # Activa el modo de pruebas
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",    # Usa una base de datos en memoria
        "SQLALCHEMY_TRACK_MODIFICATIONS": False             # Desactiva el rastreador de modificaciones ( innecesario en tests)
    }

    # Crea y configura una nueva instancia de la app para cada funcion de test
    app_instance = create_app(test_config=test_config)      # Sobreescribe la configuración por defecto con una config de prueba 
    
    with app_instance.app_context():                        # Crea un contexto de aplicacion para cada funcion de test
        db.create_all()                                     # Crea todas las tablas necesarias en la base de datos
        yield app_instance                                  # "Despierta" la instancia de la app para su uso en las funciones de test
        db.session.remove()                                 # 1. Cierra y limpia la sesión activa de SQLAlchemy
        db.drop_all()                                       # 2. Elimina todas las tablas
        db.engine.dispose()                                 # 3. Cierra todas las conexiones del pool hacia SQLite

    

@pytest.fixture
def client(app):
    """Crea y configura un cliente de prueba aislado: Provee al cliente de prueba de Flask derivado de la app creada en el fixture anterior."""
    return app.test_client()                    # El cliente de prueba isolado está listo para usar