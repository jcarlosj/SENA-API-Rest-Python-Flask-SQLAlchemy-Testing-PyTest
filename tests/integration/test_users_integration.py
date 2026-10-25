from unittest.mock import ANY

# Test: Crea un usuario con datos válidos, lo persiste en la base de datos y retorna 201
def test_create_user_with_valid_data_persists_in_db_and_returns_201(client):
    # Arrange: Configuración del caso de prueba
    path: str = "/api/v1/users"       # Ruta del endpoint que se está probando   
    payload: dict = {
        'username': 'jcarlosj',
        'email': 'jcarlosj@correo.co',
        'password': '123456789',
        'full_name': 'Juan Carlos',
        'role': 'admin'
    }
    expected_response = {
        'success': True,
        'msg': "Usuario creado satisfactoriamente",
        'data': {
            'username': payload['username'],
            'email': payload['email'],
            'full_name': payload['full_name'],
            'role': payload['role'],
            'user_id': ANY,                     # <-- Acepta cualquier valor generado
            'created_at': ANY,                  # <-- Acepta cualquier valor generado
            'updated_at': ANY                   # <-- Acepta cualquier valor generado
        }
    }   

    # Act: Realiza la petición HTTP POST a /api/v1/users
    response = client.post(path, json=payload)          # Obtiene la respuesta de la petición POST
    data = response.get_json()                          # Obtiene el JSON de la respuesta

    # Assert: Verifica que la respuesta sea correcta
    assert response.status_code == 201                  # Verifica que el código de estado sea 201 Created
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert isinstance(data['data'], dict)               # Verifica que la respuesta de la propiedad data sea un diccionario
    assert data is not None                             # Verifica que la respuesta no sea None
    assert data == expected_response                    # Verifica que la respuesta coincida con la esperada

    # Assert: Verificamos los datos retornados
    user_data = data['data']

    assert data['success'] == expected_response['success']    # Verifica que el estado sea success
    assert data['msg'] == expected_response['msg']            # Verifica que el mensaje sea el esperado

    # Assert: Verificamos los datos retornados de data
    assert user_data['username'] == payload['username']
    assert user_data['email'] == payload['email']
    assert user_data['full_name'] == payload['full_name']
    assert user_data['role'] == payload['role']

    # Assert: Verificamos los campos generados por la base de datos
    assert isinstance(user_data['user_id'], int)
    assert isinstance(user_data['created_at'], str)
    assert isinstance(user_data['updated_at'], str)

    # Assert: Verificamos que no se retorne la contraseña NUNCA
    assert 'password' not in user_data
