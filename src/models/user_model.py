from datetime import datetime
from src.models import db

class User(db.Model):
    """Modelo ORM que representa la tabla 'users'"""
    __tablename__ = 'users'

    # Define columnas de la tabla
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Método auxiliar para convertir una instancia de User en diccionario serializable a JSON"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }