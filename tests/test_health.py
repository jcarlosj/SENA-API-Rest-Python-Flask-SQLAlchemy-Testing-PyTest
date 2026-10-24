from asyncio import base_futures
import pytest
from app import app

@pytest.fixture
def client():
    """Fixture que provee un cliente de prueba aislado"""
    app.config['TESTING'] = True            # Activa el modo de prueba isolado
    with app.test_client() as client:       # Crea el contexto de prueba
        yield client                        # "Despierta"" al cliente

def test_health_checks_return_status_200(client):
    """Verifica que el endpoint /health responda con status HTTP 200 y el JSON esperado"""
    # 1. Arrange: Configuración del caso de prueba
    path: str = "/health"
    expected_data = {"status": "ok"}
    
    # 2. Act: Realiza la petición HTTP GET a /health
    response = client.get(path)
    data = response.get_json()

    # 3. Assert: Verifica que la respuesta sea correcta
    assert data is not None
    assert data['status'] == expected_data['status']
    assert response.status_code == 200  
    assert "msg" in data
    
    