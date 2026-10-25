from src.models.user_model import User
from src.models import db
from src.services.exceptions import ValidationError, ConflictError, DatabaseError, NotFoundError


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
            
    @staticmethod
    def update_user(user_id: int, data: dict) -> User:
        """
        Actualiza un usuario en el sistema
        Retorna:
            User: Instancia actualizada del usuario
        Lanza:
            ValidationError: Si faltan campos obligatorios
            ConflictError: Si el username o el email ya existen
            DatabaseError: Si ocurre un error al persistir en base de datos
            NotFoundError: Si el usuario no existe
        """
        # 1. Verificar existencia
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado", 'USER_NOT_FOUND', {'user_id': user_id})
        
        # 2. Extraer y verificar que venga al menos un campo
        new_username = data.get('username')
        new_email = data.get('email')

        if new_username is None and new_email is None:
            raise ValidationError("Debe proporcionar al menos un campo ('username' o 'email') para actualizar")

        # 3. Validar y verificar colisiones de username
        if( new_username is not None ):
            new_username = new_username.strip() if isinstance( new_username, str) else ""
            if not new_username:
                raise ValidationError("El username no puede estar vacío", 'INVALID_USERNAME', {'username': new_username})
            
            # Verificar colisión de username
            existing_user_by_username = User.query.filter_by(username=new_username).first()
            if existing_user_by_username and existing_user_by_username.user_id != user_id:
                raise ConflictError("El username ya existe", 'USER_ALREADY_EXISTS', {'username': new_username})
            
        # 4. Validar y verificar colisiones de email
        if( new_email is not None ):
            new_email = new_email.strip() if isinstance( new_email, str) else ""
            if not new_email:
                raise ValidationError("El email no puede estar vacío", 'INVALID_EMAIL', {'email': new_email})
            
            # Verificar colisión de email
            existing_user_by_email = User.query.filter_by(email=new_email).first()
            if existing_user_by_email and existing_user_by_email.user_id != user_id:
                raise ConflictError("El email ya existe", 'EMAIL_ALREADY_EXISTS', {'email': new_email})
            
        # 5. Actualizar campos si vienen en el payload
        if new_username is not None:
            user.username = new_username
        if new_email is not None:
            user.email = new_email
        
        if data.get('password') is not None:
            user.password = data.get('password')
        
        if data.get('full_name') is not None:
            user.full_name = data.get('full_name').strip() if isinstance(data.get('full_name'), str) else None
        
        if data.get('role') is not None:
            user.role = data.get('role').strip().lower() if isinstance(data.get('role'), str) else 'user'
            
        # 6. Persistir cambios en BD
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Error al actualizar usuario: {str(e)}", 'DB_ERROR', {'error': str(e)})