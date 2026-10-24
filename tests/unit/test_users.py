def test_get_all_users_returs_200_and_json(client):
    # Arrage: Configuración del caso de prueba
    path: str = "/api/v1/users"       # Ruta del endpoint que se está probando    
    expected_response = {
        'success': True,
        'msg': 'Lista de usuarios obtenida correctamente',
        'data': []
    }

    # Act: Realiza la petición HTTP GET a /api/v1/users
    response = client.get(path)                         # Obtiene la respuesta de la petición GET
    data = response.get_json()                          # Obtiene el JSON de la respuesta

    # Assert: Verifica que la respuesta sea correcta
    assert response.status_code == 200                  # Verifica que el código de estado sea 200
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert isinstance(data['data'], list)               # Verifica que la respuesta de la propiedad data sea una lista
    assert data is not None                             # Verifica que la respuesta no sea None
    assert data['success'] == expected_response['success']       # Verifica que el estado sea success
    assert data['msg'] == expected_response['msg']               # Verifica que el mensaje sea el esperado
    assert data['data'] == expected_response['data']    # Verifica que la lista de usuarios sea la esperada
    
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