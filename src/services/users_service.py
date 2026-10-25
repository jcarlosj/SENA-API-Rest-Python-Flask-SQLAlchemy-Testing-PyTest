from src.models.user_model import User
from src.models import db
from src.services.exceptions import ValidationError, ConflictError, DatabaseError


class UserService:
    # Servicio que encapsula la lógica de negocio para la entidad User


    @staticmethod
    def get_all_users():
        """
        Obtiene todos los usuarios del sistema
        Retorna:
            List[User]: Lista de instancias del modelo User
        Lanza:
            DatabaseError: Si ocurre un error al obtener los usuarios
        """
        try:
            users = User.query.all()    # 1. Obtiene todos los usuarios de la base de datos
            return users                # 2. Retorna todos los usuarios 
        except Exception as e:
            raise DatabaseError(f"Error al obtener usuarios: {str(e)}", 'DB_ERROR', {'error': str(e)})     # 3. Lanza la excepción personalizada


    @staticmethod
    def create_user(data):
        """
        Registra un nuevo usuario en el sistema
        Retorna:
            User: Instancia persistida del usuario
        Lanza:
            ValidationError: Si faltan campos o están vacios
            ConflictError: Si el username o el email ya existen
            DatabaseError: Si ocurre un error al persistir en base de datos
        """
        username = data.get('username', '').strip() if isinstance(data.get('username'), str) else ''
        email = data.get('email', '').strip() if isinstance(data.get('email'), str) else ''
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip() if isinstance(data.get('full_name'), str) else None
        role = data.get('role', '').strip() if isinstance(data.get('role'), str) else 'user'

        
        # 1. Validar campos obligatorios
        if not username or not email or not password:
            raise ValidationError("Faltan campos obligatorios", 'MISSING_REQUIRED_FIELDS', {'missing_fields': ['username', 'email', 'password']})      # Lanza la excepción de validación si faltan campos obligatorios 
        
        # 2. Validar unicidad de username y email
        if User.query.filter_by(username=username).first():
            raise ConflictError("El usuario ya existe", 'USER_ALREADY_EXISTS', {'username': username})         # Lanza la excepción de conflicto si ya existe el username
        
        if User.query.filter_by(email=email).first():
            raise ConflictError("El email ya existe", 'EMAIL_ALREADY_EXISTS', {'email': email})         # Lanza la excepción de conflicto si ya existe el email
        
        # 3. Validar campos obligatorios
        if role not in ['user', 'admin']:
            raise ValidationError("El rol no es válido", 'INVALID_ROLE', {'role': role})      # Lanza la excepción de validación si el rol no es válido

        # 3. Crear y guardar el usuario 
        new_user = User(username=username, email=email, password=password, full_name=full_name, role=role)

        try:
            db.session.add(new_user)        # 1. Añade la instancia a la sesión 
            db.session.commit()             # 2. Confirma la transacción (persistiendo en BD)
            
            return new_user                 # 3. Retorna la instancia creada
        except Exception as e:
            db.session.rollback()           # 4. Revierte la transacción en caso de error
            raise DatabaseError(f"Error al crear usuario: {str(e)}", 'DB_ERROR', {'error': str(e)})     # 5. Lanza la excepción personalizada
            