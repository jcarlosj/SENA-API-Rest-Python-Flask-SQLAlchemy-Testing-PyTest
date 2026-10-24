from flask import Blueprint, jsonify, request, Response

from src.controllers.users_controller import get_all_users_controller, get_user_by_id_controller, create_user_controller, update_user_by_id_controller, delete_user_by_id_controller

# Definición del BluePrint para el recurso users
users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
def get_all_users():
    return get_all_users_controller()

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return get_user_by_id_controller(user_id)

@users_bp.route('', methods=['POST'])
def create_user():
    return create_user_controller()

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    return update_user_by_id_controller(user_id)

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    return delete_user_by_id_controller(user_id)