from crypt import methods
from flask import Blueprint, jsonify, request

# Definición del BluePrint para el recurso users
users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
def get_all_users():
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
def get_user_by_id(user_id: int):
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
