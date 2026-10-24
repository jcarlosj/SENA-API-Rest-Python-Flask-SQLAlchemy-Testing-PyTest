import pytest

def test_health_checks_return_status_200(client):
    """Verifica que el endpoint /health responda con status HTTP 200 y el JSON esperado"""
    # 1. Arrange: Configuración del caso de prueba
    path: str = "/health"
    expected_data = {"status": "ok"}
    
    # 2. Act: Realiza la petición HTTP GET a /health
    response = client.get(path)
    data = response.get_json()

    # 3. Assert: Verifica que la respuesta sea correcta
    assert data is not None                                 # Verifica que la respuesta no sea None
    assert data['status'] == expected_data['status']        # Verifica que el estado sea 'ok'
    assert response.status_code == 200                      # Verifica que el código de estado sea 200
    assert "msg" in data                                    # Verifica que la respuesta contenga la clave 'msg'
    
def test_health_method_not_allowed(client):
    """Verifica que el endpoint /health solo acepte peticiones GET. Si un método no soportado (POST, PUT, DELETE) es usado, debe retornar un error 405 (Method Not Allowed)"""
    # 1. Arrange: Configuración del caso de prueba
    path: str = "/health"           # Ruta del endpoint que se está probando    

    # 2. Act: Realiza la petición HTTP POST a /health
    response = client.post(path)

    # 3. Assert: 
    assert response.status_code == 405

def test_health_returns_expected_fields(client):
    """
    Verifica que la respuesta del endpoint /health contenga todos los campos esperados:
    - status
    - msg
    - version
    - timestamp
    """
    # 1. Arrange: Configuración del caso de prueba
    path: str = "/health"
    expected_fields: list[str] = ["status", "msg", "version", "timestamp"]  # Campos esperados
    
    # 2. Act: Realiza la petición HTTP GET a /health
    response = client.get(path)
    data = response.get_json()

    # 3. Assert: Verifica que la respuesta sea correcta
    assert data is not None                             # Verifica que la respuesta no sea None
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert set(data.keys()) == set(expected_fields)     # Verifica que los campos sean los esperados
    assert response.status_code == 200                  # Verifica que el código de estado sea 200