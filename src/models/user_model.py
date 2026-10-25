from datetime import datetime
from sqlalchemy import inspect
from src.models import db

class User(db.Model):
    """Modelo ORM que representa la tabla 'users'"""
    __tablename__ = 'users'

    # Define columnas de la tabla
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def create_table(cls):
        """Verifica y crea la tabla en la base de datos si no existe, emitiendo un mensaje."""
        inspector = inspect(db.engine)
        if cls.__tablename__ in inspector.get_table_names():
            print(f"\033[94mℹ La tabla '{cls.__tablename__}' ya existe en la base de datos MySQL.\033[0m")
        else:
            cls.__table__.create(db.engine)
            print(f"\033[92m✔ Tabla '{cls.__tablename__}' creada exitosamente en la base de datos MySQL.\033[0m")

    def to_dict(self):
        """Método auxiliar para convertir una instancia de User en diccionario serializable a JSON"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }