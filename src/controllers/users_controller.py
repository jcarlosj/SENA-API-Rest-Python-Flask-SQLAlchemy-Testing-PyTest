from src.services.exceptions import ConflictError, ValidationError, DatabaseError
from src.services.users_service import UserService
from flask import Response, jsonify, request


def get_all_users_controller() -> tuple[Response, int]:
    """Obtiene la lista de usuarios (Read all)"""
    return (
        jsonify({
            'success': True,
            'msg': 'Lista de usuarios obtenida correctamente',
            'data': []
        }),
        200
    ) 

def get_user_by_id_controller(user_id: int) -> tuple[Response, int]:
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

def create_user_controller() -> tuple[Response, int]:
    """
        Crea un nuevo usuario (Create).
        Recibe peticion HTTP, delega al servicio y formatea la respuesta HTTP
    """

    # request.get_json(silent=True) parsea el body a un diccionario de Python.
    # Con silent=True evita lanzar un error 400 si el cliente no envía JSON válido, devolviendo None.
    payload = request.get_json(silent=True)

    # Validar que llega un JSON válido
    if payload is None:
        return jsonify({
            'success': False,
            'msg': 'El cuerpo de la petición debe ser un JSON válido'
        }), 400

    # Validar de que el payload sea un diccionario     
    if not isinstance( payload, dict ):
        return(
            jsonify({
                'success': False,
                'msg': 'El cuerpo de la petición debe ser un JSON válido'
            }),
            400
        )

    try:
        # 1. Invocación al Servicio: Retorna un objeto User
        user = UserService.create_user(data=payload)

        # 2. Formatear respuesta
        return (
            jsonify({
                'success': True,
                'msg': f"Usuario creado satisfactoriamente",
                'data': user.to_dict()
            }),
            201
        )
    except ValidationError as e:
        return jsonify({
            'success': False,
            'msg': e.message,
            'error': e.code,
            'details': e.details
        }), 400
    except ConflictError as e:
        return jsonify({
            'success': False,
            'msg': e.message,
            'error': e.code,
            'details': e.details
        }), 409
    except DatabaseError as e:
        return jsonify({
            'success': False,
            'msg': e.message,
            'error': e.code,
            'details': e.details
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': 'Error al crear usuario',
            'error': str(e)
        }), 500
        

def update_user_by_id_controller(user_id: int) -> tuple[Response, int]:
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

def delete_user_by_id_controller(user_id: int) -> tuple[Response, int]:
    """Elimina un usuario por su ID (Delete)."""
    return (
        jsonify({
            'success': True,
            'msg': f'Usuario con ID {user_id} eliminado correctamente'
        }),
        200
    )   