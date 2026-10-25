from unittest.mock import ANY

def test_get_all_users_when_users_exist_returns_200_and_users_list(client):
    # Arrange: Configuración del caso de prueba
    path: str = "/api/v1/users"       # Ruta del endpoint que se está probando   
    user_1 = {
        'username': 'ana',
        'email': 'ana.castro@correo.co',
        'password': '123456789',
        'full_name': 'Ana Castro',
        'role': 'user'
    }
    user_2 = {
        'username': 'caro',
        'email': 'cporras@correo.co',
        'password': '123456789',
        'full_name': 'Carolina Porras',
        'role': 'admin'
    }

    # 1. Crea usuarios para la prueba
    client.post( path, json=user_1 )                    # 1. Crea el usuario 1
    client.post( path, json=user_2 )                    # 2. Crea el usuario 2

    # Act: Realiza la petición HTTP GET a /api/v1/users
    response = client.get(path)                         # Obtiene la respuesta de la petición GET
    data = response.get_json()                          # Obtiene el JSON de la respuesta

    # Assert: Verifica que la respuesta sea correcta
    assert response.status_code == 200                  # Verifica que el código de estado sea 200 OK
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert isinstance(data['data'], list)               # Verifica que la respuesta de la propiedad data sea una lista
    assert data is not None                             # Verifica que la respuesta no sea None

    # Assert: Verificamos los datos retornados
    users_list = data['data']                           # Obtiene la lista de usuarios de la respuesta

    assert data['success'] is True                                   # Verifica que el estado sea success
    assert data['msg'] == "Usuarios obtenidos satisfactoriamente"    # Verifica que el mensaje sea el esperado

    
    # Assert: Validamos los datos de los usuarios retornados
    for user in users_list:
        # Verifica que los campos obligatorios estén presentes
        assert user['username']
        assert user['email']
        assert user['full_name']
        assert user['role']
        assert user['user_id']
        assert user['created_at']
        assert user['updated_at']
        
        # Verifica que los campos obligatorios sean del tipo correcto
        assert isinstance(user['username'], str)
        assert isinstance(user['email'], str)
        assert isinstance(user['full_name'], str)
        assert isinstance(user['role'], str)
        assert isinstance(user['user_id'], int)
        assert isinstance(user['created_at'], str)
        assert isinstance(user['updated_at'], str)
        
        # Verificamos que el username y el role sean correctos
        assert user['username'] in ['ana', 'caro']
        assert user['role'] in ['user', 'admin']

    # Validamos que los usuarios existan en la lista
    usernames = [user['username'] for user in users_list]
    assert 'ana' in usernames
    assert 'caro' in usernames


    # Assert: Verificamos que la propiedad data sea una lista
    assert isinstance(users_list, list)                 # Verifica que la respuesta de la propiedad data sea una lista
    assert len(users_list) == 2                         # Verifica que la respuesta de la propiedad data tenga 2 elementos
    
    
    # Assert: Verificamos que NINGÚN usuario exponga su password
    for user in users_list:
        assert 'password' not in user                   # Verifica que cada usuario de la lista no retorne el password
        assert isinstance(user['user_id'], int)
        assert isinstance(user['created_at'], str)
        assert isinstance(user['updated_at'], str)
    

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
    assert data['success'] is True                      # Verifica que el estado sea success
    assert isinstance(data, dict)                       # Verifica que la respuesta sea un diccionario
    assert isinstance(data['data'], dict)               # Verifica que la respuesta de la propiedad data sea un diccionario
    assert data is not None                             # Verifica que la respuesta no sea None
    assert data == expected_response                    # Verifica que la respuesta coincida con la esperada

    # Assert: Verificamos los datos retornados
    user_data = data['data']                            # Obtiene la propiedad data de la respuesta

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
