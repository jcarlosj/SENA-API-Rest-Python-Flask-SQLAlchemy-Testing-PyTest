from typing import AnyStr
from unittest.mock import ANY

   
def test_get_user_by_id_returns_200_and_json(client):
    # Arrage: Configuración del caso de prueba
    user_id: int = 2    # ID del usuario que se está probando
    path: str = f"/api/v1/users/{user_id}"       # Ruta del endpoint que se está probando    
    expected_response = {
        'success': True,
        'msg': f'Usuario con ID {user_id} obtenido correctamente',
        'data': {
            'id': user_id
        }
    }

    # Act: Realiza la petición HTTP GET a /api/v1/users
    response = client.get(path)                         # Obtiene la respuesta de la petición GET
    data = response.get_json()                          # Obtiene el JSON de la respuesta

    # Assert: Verifica que la respuesta sea correcta
    assert response.status_code == 200                  # Verifica que el código de estado sea 200
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert isinstance(data['data'], dict)               # Verifica que la respuesta de la propiedad data sea un diccionario
    assert data is not None                             # Verifica que la respuesta no sea None
    assert data['success'] == expected_response['success']    # Verifica que el estado sea success
    assert data['msg'] == expected_response['msg']            # Verifica que el mensaje sea el esperado
    assert data['data'] == expected_response['data']          # Verifica que los datos de usuarios sea la esperados


def test_delete_user_returns_200_and_json(client):
    # Arrange: Configuración del caso de prueba
    # 1. Se crean usuarios previos para asegurar que el ID 2 exista en la base de datos
    client.post("/api/v1/users", json={'username': 'temp1', 'email': 'temp1@correo.co', 'password': '123'})
    client.post("/api/v1/users", json={'username': 'temp2', 'email': 'temp2@correo.co', 'password': '123'})
    user_id: int = 2    # ID del usuario que se está probando
    path: str = f"/api/v1/users/{user_id}"       # Ruta del endpoint que se está probando    
    expected_response = {
        'success': True,
        'msg': f'Usuario con ID {user_id} eliminado correctamente',
        'data': {
            'id': user_id
        }
    }

    # Act: Realiza la petición HTTP DELETE a /api/v1/users
    response = client.delete(path)           # Obtiene la respuesta de la petición GET
    data = response.get_json()                          # Obtiene el JSON de la respuesta

    # Assert: Verifica que la respuesta sea correcta
    assert response.status_code == 200                  # Verifica que el código de estado sea 200
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert data is not None                             # Verifica que la respuesta no sea None
    assert data['success'] == expected_response['success']    # Verifica que el estado sea success
    assert data['msg'] == expected_response['msg']            # Verifica que el mensaje sea el esperado