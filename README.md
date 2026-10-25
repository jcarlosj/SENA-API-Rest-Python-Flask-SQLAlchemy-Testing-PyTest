# API Backend con Flask y Testing 

Backend desarrollado en Python con Flask siguiendo el patrón de arquitectura **Application Factory** y **Blueprints**, con configuración para base de datos MySQL (SQLAlchemy) y suite de pruebas unitarias automáticas con métricas de cobertura en Pytest.

---

## 📋 Requisitos Previos

Asegúrate de tener instalado en tu sistema:
- **Python 3.10+** (Recomendado 3.12 o 3.14)
- **Git**
- **MySQL Server** (o MariaDB) ejecutándose localmente o en contenedor Docker

---

## 🚀 Guía de Inicio Rápido (Paso a Paso)

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd BackEnd
```

---

### 2. Crear y activar el entorno virtual (`venv`)
Es fundamental aislar las dependencias del proyecto:

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar en Linux / macOS:
source venv/bin/activate

# Activar en Windows (PowerShell):
# .\venv\Scripts\Activate.ps1
```

---

### 3. Instalar dependencias
Con el entorno virtual activado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 📦 Tabla de Dependencias del Proyecto

| Dependencia | Comando de Instalación | Tipo | ¿Para qué se usa en el proyecto? |
| :--- | :--- | :--- | :--- |
| **`Flask`** | `pip install Flask` | Núcleo | Framework web principal. Gestiona las rutas (Blueprints), peticiones HTTP, respuestas JSON y ciclo de vida de la API. |
| **`python-dotenv`** | `pip install python-dotenv` | Configuración | Carga automáticamente las variables de entorno desde el archivo `.env` al sistema (`os.getenv`), como credenciales de base de datos y puertos. |
| **`SQLAlchemy`** | `pip install SQLAlchemy` | Base de Datos | ORM y Toolkit SQL. Crea motores de conexión (`create_engine`), ejecuta consultas y abstrae la comunicación con la base de datos. |
| **`PyMySQL`** | `pip install PyMySQL` | Driver de BD | Conector/driver en Python puro para MySQL. Permite a SQLAlchemy dialogar con servidores MySQL/MariaDB (`mysql+pymysql://...`). |
| **`cryptography`** | `pip install cryptography` | Seguridad | Requerido por PyMySQL para autenticación segura moderna (método `caching_sha2_password` estándar en MySQL 8+). |
| **`pytest`** | `pip install pytest` | Testing | Framework para escribir y ejecutar pruebas unitarias automáticas de endpoints y funciones. |
| **`pytest-cov`** | `pip install pytest-cov` | Testing | Extensión de Pytest que calcula métricas de cobertura de código (porcentaje de líneas evaluadas) y genera reportes en terminal y HTML. |

> **Nota:** Librerías como `Werkzeug`, `Jinja2`, `click`, `coverage` o `blinker` son instaladas automáticamente por pip como subdependencias de las anteriores.


---

### 4. Configurar las Variables de Entorno (`.env`)
El repositorio incluye una plantilla [.env.example](.env.example). Crea tu archivo local `.env`:

```bash
cp .env.example .env
```

Abre `.env` y ajusta tus credenciales locales de MySQL:

```env
FLASK_ENV=development
DB_USER=flask_user        # O root
DB_PASSWORD=tu_password   # La contraseña de tu usuario de MySQL
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mi_api_flask_db
```

> [!NOTE]
> Para la configuración detallada de MySQL, creación de la base de datos y usuarios (root vs usuario dedicado), consulta la guía en: [docs/mysql_setup_guide.md](docs/mysql_setup_guide.md).

---

### 5. Ejecutar la Aplicación

Para iniciar el servidor de desarrollo en `http://localhost:5000`:

```bash
python -m src.app
```

> [!IMPORTANT]
> Ejecuta siempre con **`python -m src.app`** (como módulo) para que Python resuelva correctamente la raíz del proyecto y las rutas relativas.

Al arrancar, el servidor verificará la conexión a la base de datos MySQL y mostrará el estado en la consola:
```text
✔ Conexión a la base de datos MySQL establecida con éxito.
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🧪 Pruebas Unitarias y Cobertura (`pytest`)

El proyecto cuenta con configuración predefinida en [pytest.ini](pytest.ini).

### Ejecutar todas las pruebas:
```bash
pytest -v
```

### Ejecutar pruebas con reporte de cobertura en terminal:
```bash
pytest --cov=src --cov-report=term-missing
```

### Generar y ver reporte de cobertura HTML interactivo:
```bash
pytest --cov=src --cov-report=html

# Abrir el reporte en el navegador (Linux):
xdg-open htmlcov/index.html
# O arrastra htmlcov/index.html a cualquier navegador web.
```

---

## 📁 Estructura del Proyecto

```text
BackEnd/
├── docs/                      # Guías de configuración y arquitectura
│   └── mysql_setup_guide.md   # Guía paso a paso para configurar MySQL
├── src/                       # Código fuente de la aplicación
│   ├── config/                # Módulos de configuración (MySQL, variables .env)
│   ├── controllers/           # Lógica de negocio de cada recurso
│   ├── routes/                # Blueprints y definiciones de endpoints
│   └── app.py                 # Application Factory (create_app) y entrypoint
├── tests/                     # Suite de pruebas automáticas
│   ├── conftest.py            # Fixtures compartidos de Pytest (app, client)
│   └── unit/                  # Pruebas unitarias (test_health, test_users)
├── bruno/                     # Colección de peticiones HTTP en Bruno
├── .env.example               # Plantilla de variables de entorno
├── pytest.ini                 # Configuración de Pytest y pytest-cov
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Esta documentación
```

---

## 🛠 Endpoints Disponibles

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/health` | Chequeo de salud del servicio |
| `GET` | `/api/v1/users` | Listar todos los usuarios |
| `GET` | `/api/v1/users/<id>` | Obtener usuario por ID |
| `POST` | `/api/v1/users` | Crear un nuevo usuario |
| `PUT` | `/api/v1/users/<id>` | Actualizar usuario por ID |
| `DELETE` | `/api/v1/users/<id>` | Eliminar usuario por ID |
