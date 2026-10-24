from flask import Blueprint, jsonify, request, Response

# Definición del BluePrint para el recurso users
users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
def get_all_users() -> tuple[Response, int]:
    """Obtiene la lista de usuarios (Read all)"""
    return (
        jsonify({
            'success': True,
            'msg': 'Lista de usuarios obtenida correctamente',
            'data': []
        }),
        200
    ) 

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id: int) -> tuple[Response, int]:
    """Obtiene un usuario por su ID (Read one)"""
    return (
        jsonify({
            'success': True,
            'msg': f'Usuario con ID {user_id} obtenido correctamente',
            'data': {
                'id': user_id
            }
        }),
        200
    ) 

@users_bp.route('', methods=['POST'])
def create_user() -> tuple[Response, int]:
    """Crea un nuevo usuario (Create)."""

    # request.get_json(silent=True) parsea el body a un diccionario de Python.
    # Con silent=True evita lanzar un error 400 si el cliente no envía JSON válido, devolviendo None.
    payload = request.get_json(silent=True)

    # Validación básica de que llegó un JSON válido
    if payload is None:
        return jsonify({
            'success': False,
            'msg': 'El cuerpo de la petición debe ser un JSON válido'
        }), 400
    
    # Ahora puedes acceder a los campos que envió el cliente:
    name = payload.get('name')
    email = payload.get('email')

    return (
        jsonify({
            'success': True,                                # Estado de la petición
            'msg': f"Usuario '{ name }' creado satisfactoriamente",     # Mensaje de confirmación
            'data': payload                                 # Datos del usuario creado
        }),
        201,                                                # Código de estado HTTP 201 Created
    )

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> tuple[Response, int]:
    """Actualiza un usuario por su ID (Update)."""

    # request.get_json(silent=True) parsea el body a un diccionario de Python.
    # Con silent=True evita lanzar un error 400 si el cliente no envía JSON válido, devolviendo None.
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            'success': False,
            'msg': 'El cuerpo de la petición debe ser un JSON válido'
        }), 400

    name = payload.get('name')
    email = payload.get('email')

    return (
        jsonify({
            'success': True,
            'msg': f'Usuario con ID {user_id} actualizado correctamente',
            'data': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }),
        200
    ) 

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> tuple[Response, int]:
    """Elimina un usuario por su ID (Delete)."""
    return (
        jsonify({
            'success': True,
            'msg': f'Usuario con ID {user_id} eliminado correctamente',
            'data': {
                'id': user_id
            }
        }),
        200
    ) 