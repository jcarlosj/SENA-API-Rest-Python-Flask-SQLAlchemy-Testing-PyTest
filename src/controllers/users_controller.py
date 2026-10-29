from src.services.exceptions import ConflictError, ValidationError, DatabaseError, NotFoundError
from src.services.users_service import UserService
from flask import Response, jsonify, request


def get_all_users_controller() -> tuple[Response, int]:
    """Obtiene la lista de usuarios (Read all)"""

    try:
        users = UserService.get_all_users()
        users_list = [user.to_dict() for user in users]
        return (
            jsonify({
                'success': True,
                'msg': 'Usuarios obtenidos satisfactoriamente',
                'data': users_list
            }),
            200
        )
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
            'msg': 'Error al obtener usuarios',
            'error': str(e)
        }), 500

def get_user_by_id_controller(user_id: int) -> tuple[Response, int]:
    """Obtiene un usuario por su ID (Read one)."""
    try:
        user = UserService.get_user_by_id(user_id)
        return (
            jsonify({
                'success': True,
                'msg': f'Usuario con ID {user_id} obtenido correctamente',
                'data': user.to_dict()
            }),
            200
        )
    except NotFoundError as err:
        return (
            jsonify({
                'success': False,
                'msg': err.message,
                'error': err.code,
                'details': err.details
            }),
            404
        )
    except DatabaseError as err:
        return (
            jsonify({
                'success': False,
                'msg': err.message,
                'error': err.code,
                'details': err.details
            }),
            500
        )
    except Exception as e:
        return (
            jsonify({
                'success': False,
                'msg': 'Ocurrió un error inesperado al obtener el usuario.',
                'error': str(e)
            }),
            500
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
        print( f'create user >>> {user.to_dict()}' )

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

    if not isinstance(payload, dict):
        return (
            jsonify({
                "status": "error",
                "msg": "El cuerpo de la petición debe ser un objeto JSON válido.",
            }),
            400,
        )

    try:
        updated_user = UserService.update_user(user_id, payload)
        return (
            jsonify({
                "success": True,
                "msg": f"Usuario con ID {user_id} actualizado correctamente",
                "data": updated_user.to_dict(),
            }),
            200,
        )
    except NotFoundError as err:
        return jsonify({"success": False, "msg": err.message, "error": err.code, "details": err.details}), 404
    except ValidationError as err:
        return jsonify({"success": False, "msg": err.message, "error": err.code, "details": err.details}), 400
    except ConflictError as err:
        return jsonify({"success": False, "msg": err.message, "error": err.code, "details": err.details}), 409
    except DatabaseError as err:
        return jsonify({"success": False, "msg": err.message, "error": err.code, "details": err.details}), 500
    except Exception as e:
        return (
            jsonify({
                "success": False,
                "msg": "Ocurrió un error inesperado al actualizar el usuario.",
                "error": str(e)
            }),
            500,
        )

def delete_user_by_id_controller(user_id: int) -> tuple[Response, int]:
    """Elimina un usuario por su ID (Delete)."""
    try:
        deleted_user = UserService.delete_user(user_id)
        return (
            jsonify({
                'success': True,
                'msg': f'Usuario con ID {user_id} eliminado correctamente',
                'data': deleted_user.to_dict()
            }),
            200
        )
    except NotFoundError as err:
        return (
            jsonify({
                'success': False,
                'msg': err.message,
                'error': err.code,
                'details': err.details
            }),
            404
        )
    except DatabaseError as err:
        return (
            jsonify({
                'success': False,
                'msg': err.message,
                'error': err.code,
                'details': err.details
            }),
            500
        )
    except Exception as e:
        return (
            jsonify({
                'success': False,
                'msg': 'Ocurrió un error inesperado al eliminar el usuario.',
                'error': str(e)
            }),
            500
        )