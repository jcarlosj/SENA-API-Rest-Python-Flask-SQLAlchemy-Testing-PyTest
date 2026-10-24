import pytest
from src.app import create_app

"""Pytest reconoce automáticamente un archivo especial llamado tests/conftest.py. Cualquier fixture declarado allí queda disponible para todos los archivos de prueba del proyecto sin necesidad de importarlo manualmente."""

@pytest.fixture
def app():
    """Crea y configura una nueva instancia de la app para cada funcion de test"""
    app_instance = create_app({'TESTING': True})    # Sobreescribe la configuración por defecto con una config de prueba 
    yield app_instance                              # "Despierta" la instancia de la app para su uso en las funciones de test

@pytest.fixture
def client(app):
    """Crea y configura un cliente de prueba aislado: Provee al cliente de prueba de Flask derivado de la app creada en el fixture anterior."""
    return app.test_client()                    # El cliente de prueba isolado está listo para usar