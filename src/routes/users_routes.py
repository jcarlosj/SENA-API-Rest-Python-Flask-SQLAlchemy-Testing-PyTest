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

