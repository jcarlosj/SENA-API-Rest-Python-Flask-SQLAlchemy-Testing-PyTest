# Formato estandar de una cadena de conexion en MySQL con PySQLAlchemy
# mysql+pymysql://<usuario>:<password>@<host>:<puerto>/<nombre_bd>
# mysql+pymysql://root:secret@localhost:3306/mi_api_flask_db

import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env local
load_dotenv()


class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_default")

    # Credenciales de conexión a MySQL
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "mi_api_flask_db")

    # URI de SQLAlchemy para conectarse a MySQL mediante PyMySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Desactiva avisos innecesarios de eventos de SQLAlchemy para ahorrar memoria
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def verify_database_connection(uri: str) -> bool:
    """Verifica si la conexión a la base de datos es exitosa ejecutando un ping simple."""
    try:
        from sqlalchemy import create_engine, text

        # Crear motor de conexión
        engine = create_engine(uri)

        # Verificar conexión
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
        print("\033[92m✔ Conexión a la base de datos MySQL establecida con éxito.\033[0m")
        return True
    except Exception as error:
        print(f"\033[91m✖ Error al conectar con la base de datos MySQL:\033[0m {error}")
        return False