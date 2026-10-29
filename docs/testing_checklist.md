# 📋 Checklist de Pruebas Unitarias y de Integración

Este documento detalla el inventario exhaustivo de las pruebas unitarias y de integración aplicables a todas las funcionalidades desarrolladas hasta el momento en la API REST (Flask + SQLAlchemy + PyTest). 

Cada ítem cuenta con su respectiva casilla de verificación:
- **`[x]` Implementada y Pasando:** La prueba existe en el código, está activa y pasa exitosamente en la suite de pruebas (`pytest`).
- **`[ ]` Pendiente / Por Implementar:** Escenario de prueba identificado (casos borde, validaciones, errores de negocio, excepciones de base de datos o funcionalidades pendientes en la capa de servicio).

---

## 📊 Resumen Ejecutivo del Estado del Testing

| Métrica | Valor Actual |
| :--- | :--- |
| **Pruebas Totales Identificadas** | 62 |
| **Pruebas Implementadas y Exitosas (`[x]`)** | 13 |
| **Pruebas Pendientes (`[ ]`)** | 49 |
| **Porcentaje de Cobertura de Código (`pytest-cov`)** | 69% |
| **Estado de la Suite (`pytest`)** | 15 Passed (100% de las pruebas existentes pasan) |
| **Motor de BD en Pruebas** | SQLite en memoria (`sqlite:///:memory:`) vía fixture en `tests/conftest.py` |

---

## 1. Módulo Health Check (`/health`)

Valida el estado operativo de la API, versión y timestamp del sistema.

### 1.1 Pruebas Unitarias
- [x] **Retorno exitoso con status 200 y confirmación de estado:** Valida que `GET /health` responda HTTP 200 y contenga `"status": "ok"` y clave `"msg"`.  
  *Referencia:* `tests/unit/test_health.py::test_health_checks_return_status_200`
- [x] **Métodos HTTP no permitidos (405):** Valida que peticiones `POST /health` sean rechazadas con código HTTP 405 Method Not Allowed.  
  *Referencia:* `tests/unit/test_health.py::test_health_method_not_allowed`
- [x] **Estructura exacta de campos JSON:** Valida que el payload de respuesta contenga exactamente las claves `["status", "msg", "version", "timestamp"]`.  
  *Referencia:* `tests/unit/test_health.py::test_health_returns_expected_fields`
- [x] **Otros métodos HTTP no permitidos:** Validar que peticiones `PUT`, `DELETE` y `PATCH` sobre `/health` retornen 405 Method Not Allowed.  
  *Referencia:* `tests/unit/test_health.py::test_health_unsupported_methods_return_405`
- [ ] **Formato de marca temporal (timestamp):** Validar que el campo `timestamp` corresponda a una cadena en formato ISO 8601 válido y parseable.
- [ ] **Formato de versión:** Validar que el campo `version` cumpla con formato semántico (ej. `"1.0.0"`).
- [ ] **Cabeceras de respuesta:** Validar que la cabecera `Content-Type` sea `application/json`.

### 1.2 Pruebas de Integración
- [x] **Accesibilidad del endpoint en el contexto de la aplicación:** Verifica que la ruta `/health` esté correctamente montada y accesible mediante el cliente de pruebas.  
  *Referencia:* `tests/integration/test_endpoints_integration.py::test_health_endpoint_is_accessible`

---

## 2. Enrutamiento General e Infraestructura (`src/app.py`)

Garantiza el correcto registro de Blueprints, manejo de errores de rutas y Application Factory.

### 2.1 Pruebas de Integración y Enrutamiento
- [x] **Ruta inexistente (404 Not Found):** Valida que peticiones a rutas no registradas (ej. `/api/v1/ruta-inexistente`) respondan HTTP 404.  
  *Referencia:* `tests/integration/test_endpoints_integration.py::test_url_not_found`
- [x] **Registro de reglas en `url_map`:** Valida que las rutas esperadas (`/health`, `/api/v1/users`, `/api/v1/users/<int:user_id>`) estén registradas en el mapa de enrutamiento de Flask.  
  *Referencia:* `tests/integration/test_endpoints_integration.py::test_expected_routes_are_registered`
- [ ] **Manejo de rutas mal formadas:** Valida que llamadas a `/api/v1/users/<id>` con valores no numéricos (ej. `/api/v1/users/abc`) respondan 404 por regla de tipo `<int:user_id>`.
- [ ] **Application Factory sin configuración de prueba:** Validar que `create_app()` inicialice correctamente con la configuración base (`Config`).
- [ ] **Application Factory con inyección dinámica:** Validar que parámetros personalizados en `test_config` sobreescriban adecuadamente la configuración de la app.

---

## 3. Módulo de Usuarios (`/api/v1/users`)

### 3.1 Obtener Todos los Usuarios (`GET /api/v1/users`)

#### Pruebas de Integración
- [x] **Listar usuarios existentes (200 OK):** Valida que al existir usuarios en base de datos, retorne HTTP 200, `success: True`, lista con los registros creados, tipos de datos correctos y **sin exponer el campo `password`**.  
  *Referencia:* `tests/integration/test_users_integration.py::test_get_all_users_when_users_exist_returns_200_and_users_list`
- [x] **Accesibilidad de la URL base de usuarios:** Valida que `/api/v1/users` responda HTTP 200 OK.  
  *Referencia:* `tests/integration/test_endpoints_integration.py::test_users_endpoint_is_accessible`
- [ ] **Base de datos vacía:** Valida que al no haber usuarios registrados en la base de datos, retorne HTTP 200, `success: True` y `data: []` (lista vacía).

#### Pruebas Unitarias (Controlador / Servicio Aislado)
- [ ] **Manejo de error de base de datos (`DatabaseError`):** Simular fallo en `UserService.get_all_users` y verificar que el controlador responda HTTP 500 con formato de error estándar.
- [ ] **Manejo de excepción genérica inesperada:** Simular fallo genérico `Exception` y verificar respuesta HTTP 500.

---

### 3.2 Crear Usuario (`POST /api/v1/users`)

#### Pruebas de Integración (Persistencia + HTTP)
- [x] **Creación exitosa con datos válidos (201 Created):** Valida persistencia en base de datos, retorno HTTP 201, campos autogenerados (`user_id`, `created_at`, `updated_at`), coincidencia de datos y **omisión de `password`** en la respuesta.  
  *Referencia:* `tests/integration/test_users_integration.py::test_create_user_with_valid_data_persists_in_db_and_returns_201`
- [ ] **Cuerpo de petición no es JSON (400 Bad Request):** Enviar cuerpo vacío o texto plano (`payload is None`) y verificar retorno 400 con mensaje de validación.
- [ ] **Cuerpo de petición no es un diccionario JSON (400 Bad Request):** Enviar un array JSON `[]` o primitivo y verificar retorno 400.
- [ ] **Validación de campo obligatorio faltante - `username` (400 Bad Request):** Omitir o enviar vacío `username`, validar código `MISSING_REQUIRED_FIELDS`.
- [ ] **Validación de campo obligatorio faltante - `email` (400 Bad Request):** Omitir o enviar vacío `email`, validar código `MISSING_REQUIRED_FIELDS`.
- [ ] **Validación de campo obligatorio faltante - `password` (400 Bad Request):** Omitir o enviar vacío `password`, validar código `MISSING_REQUIRED_FIELDS`.
- [ ] **Conflicto por `username` duplicado (409 Conflict):** Intentar registrar un usuario con `username` existente y validar código `USER_ALREADY_EXISTS`.
- [ ] **Conflicto por `email` duplicado (409 Conflict):** Intentar registrar un usuario con `email` existente y validar código `EMAIL_ALREADY_EXISTS`.
- [ ] **Validación de rol inválido (400 Bad Request):** Enviar rol diferente a `'user'` o `'admin'` (ej. `'superadmin'`) y validar código `INVALID_ROLE`.
- [ ] **Rol por defecto:** Crear usuario sin especificar `role` y validar que se asigne automáticamente `'user'`.
- [ ] **Campo opcional `full_name`:** Crear usuario con `full_name: null` o sin él y verificar creación exitosa.
- [ ] **Sanitización de cadenas (espacios en blanco):** Enviar campos con espacios circundantes y validar que se guarden recortados (`strip`).

#### Pruebas Unitarias (Controlador / Servicio Aislado)
- [ ] **Rollback en fallo de base de datos:** Simular fallo de base de datos en commit y verificar que se ejecute `rollback` y se retorne HTTP 500 (`DatabaseError`).
- [ ] **Manejo de excepción no controlada:** Simular error imprevisto y validar retorno HTTP 500.

---

### 3.3 Actualizar Usuario (`PUT /api/v1/users/<id>`)

#### Pruebas de Integración (Persistencia + HTTP)
- [x] **Actualización exitosa con datos válidos (200 OK):** Valida actualización en base de datos, retorno HTTP 200, integridad de datos devueltos y **omisión de `password`**.  
  *Referencia:* `tests/integration/test_users_integration.py::test_update_user_with_valid_data_persists_in_db_and_returns_200`
- [ ] **Cuerpo no es un objeto JSON (400 Bad Request):** Enviar cuerpo que no sea diccionario y verificar código 400.
- [ ] **Usuario no encontrado (404 Not Found):** Intentar actualizar un `user_id` inexistente y verificar código `USER_NOT_FOUND` (404).
- [ ] **Petición sin campos a actualizar (400 Bad Request):** Enviar payload sin `username` ni `email` y verificar error de validación.
- [ ] **Validación de `username` vacío en actualización (400 Bad Request):** Enviar `username: ""` y validar código `INVALID_USERNAME`.
- [ ] **Validación de `email` vacío en actualización (400 Bad Request):** Enviar `email: ""` y validar código `INVALID_EMAIL`.
- [ ] **Conflicto por `username` ocupado por otro usuario (409 Conflict):** Intentar cambiar el `username` al de otro usuario existente y validar código `USER_ALREADY_EXISTS`.
- [ ] **Conflicto por `email` ocupado por otro usuario (409 Conflict):** Intentar cambiar el `email` al de otro usuario existente y validar código `EMAIL_ALREADY_EXISTS`.
- [ ] **Conservación de propios datos sin conflicto (Idempotencia de colisión):** Actualizar enviando el mismo `username` o `email` del propio usuario sin que dispare error 409.
- [ ] **Actualización parcial:** Actualizar únicamente el `username` sin enviar `email`, o viceversa.
- [ ] **Actualización de campos secundarios:** Validar actualización de `full_name`, `password` y `role` (con conversión a minúsculas).

#### Pruebas Unitarias (Controlador / Servicio Aislado)
- [ ] **Rollback de sesión en error de commit:** Simular fallo en `db.session.commit()` y verificar llamada a `db.session.rollback()` y lanzamiento de `DatabaseError`.
- [ ] **Respuesta HTTP 500 ante `DatabaseError`:** Verificar formato y código HTTP 500 retornado por el controlador.

---

### 3.4 Obtener Usuario por ID (`GET /api/v1/users/<id>`)

> [!NOTE]
> **Estado de la funcionalidad en el código:**  
> El controlador `get_user_by_id_controller` está actualmente implementado como un **stub/mock** que devuelve datos fijos sin consultar la base de datos ni invocar a `UserService`. La prueba unitaria existente valida únicamente la respuesta mockeada actual.

#### Pruebas Unitarias (Estado Actual)
- [x] **Respuesta simulada con status 200:** Verifica que el endpoint retorne HTTP 200 y el JSON mock con `{'id': user_id}`.  
  *Referencia:* `tests/unit/test_users.py::test_get_user_by_id_returns_200_and_json`

#### Pruebas de Integración y Servicio (Pendientes de implementar funcionalidad completa)
- [ ] **Consulta exitosa de usuario existente en BD (200 OK):** Consultar un usuario persistido y validar que devuelva su objeto completo sin `password`.
- [ ] **Usuario inexistente (404 Not Found):** Consultar un ID que no exista y verificar respuesta 404 con código `USER_NOT_FOUND`.
- [ ] **ID de usuario inválido en URL (404 Not Found):** Enviar ID alfanumérico en ruta y verificar rechazo por Flask.
- [ ] **Manejo de errores de base de datos (500 Internal Server Error):** Validar respuesta ante fallo de conexión o consulta en base de datos.

---

### 3.5 Eliminar Usuario por ID (`DELETE /api/v1/users/<id>`)

> [!NOTE]
> **Estado de la funcionalidad en el código:**  
> El controlador `delete_user_by_id_controller` está actualmente implementado como un **stub/mock** que responde confirmación estática sin interactuar con la base de datos ni invocar a `UserService`. La prueba unitaria existente valida únicamente este mock.

#### Pruebas Unitarias (Estado Actual)
- [x] **Respuesta simulada con status 200:** Verifica que `DELETE /api/v1/users/2` retorne HTTP 200 y mensaje de confirmación de eliminación simulado.  
  *Referencia:* `tests/unit/test_users.py::test_delete_user_returns_200_and_json`

#### Pruebas de Integración y Servicio (Pendientes de implementar funcionalidad completa)
- [ ] **Eliminación real y persistente en BD (200 OK):** Eliminar un usuario existente, verificar confirmación y verificar que ya no exista en base de datos.
- [ ] **Verificación de eliminación con consulta posterior (404):** Intentar un `GET /api/v1/users/<id>` posterior al borrado y verificar que responda 404.
- [ ] **Eliminar usuario inexistente (404 Not Found):** Intentar eliminar un ID no existente y verificar respuesta 404 `USER_NOT_FOUND`.
- [ ] **ID de usuario inválido en URL (404 Not Found):** Enviar ID alfanumérico en ruta y verificar rechazo.
- [ ] **Rollback y manejo de fallo en eliminación (500 Internal Server Error):** Simular fallo en `db.session.commit()` durante el borrado.

---

## 4. Capa de Lógica de Negocio y Servicios (`UserService`)

Pruebas unitarias directas sobre la clase `UserService` aislando dependencias mediante mocks de SQLAlchemy (`db.session` y `User.query`).

### 4.1 Método `UserService.get_all_users`
- [ ] **Retorno de lista de usuarios:** Valida retorno correcto de colección de modelos `User`.
- [ ] **Lanzamiento de `DatabaseError`:** Valida que si `User.query.all()` arroja excepción, el método capture y relance `DatabaseError` con detalles y código `DB_ERROR`.

### 4.2 Método `UserService.create_user`
- [ ] **Lógica de validación de campos obligatorios faltantes:** Valida lanzamiento de `ValidationError`.
- [ ] **Detección de conflicto por username existente:** Valida lanzamiento de `ConflictError`.
- [ ] **Detección de conflicto por email existente:** Valida lanzamiento de `ConflictError`.
- [ ] **Validación de roles permitidos:** Valida lanzamiento de `ValidationError` ante rol inválido.
- [ ] **Manejo de transacción y rollback:** Valida que ante excepción en `commit()`, se invoque `rollback()` y se lance `DatabaseError`.

### 4.3 Método `UserService.update_user`
- [ ] **Usuario no encontrado en sesión (`db.session.get`):** Valida lanzamiento de `NotFoundError`.
- [ ] **Validación de payload sin datos:** Valida lanzamiento de `ValidationError`.
- [ ] **Validación de colisión de username contra otros registros:** Valida lanzamiento de `ConflictError` solo si el ID difiere.
- [ ] **Validación de colisión de email contra otros registros:** Valida lanzamiento de `ConflictError` solo si el ID difiere.
- [ ] **Manejo de rollback en error de persistencia:** Valida ejecución de `db.session.rollback()` y lanzamiento de `DatabaseError`.

### 4.4 Métodos Pendientes de Desarrollo en `UserService`
- [ ] **Implementación y prueba de `UserService.get_user_by_id(user_id)`:**
  - Retorno de instancia `User` si existe.
  - Lanzamiento de `NotFoundError` si no existe.
  - Lanzamiento de `DatabaseError` ante error de consulta.
- [ ] **Implementación y prueba de `UserService.delete_user(user_id)`:**
  - Borrado y confirmación exitosa de la transacción.
  - Lanzamiento de `NotFoundError` si no existe el registro.
  - Rollback y lanzamiento de `DatabaseError` ante fallo de commit.

---

## 5. Capa de Modelo y Persistencia (`User` - SQLAlchemy ORM)

Pruebas sobre el modelo ORM `src/models/user_model.py`.

### 5.1 Pruebas Unitarias del Modelo
- [ ] **Instanciación y valores por defecto:** Validar que al instanciar `User()`, el campo `role` tome por defecto el valor `'user'`.
- [ ] **Serialización con `to_dict()`:** Validar que `to_dict()` devuelva diccionario con claves `user_id`, `username`, `email`, `full_name`, `role`, `created_at`, `updated_at`.
- [ ] **Seguridad en `to_dict()` (Exclusión de contraseña):** Validar estrictamente que `'password'` **nunca** esté presente en el diccionario resultante.
- [ ] **Serialización con fechas nulas:** Validar que si `created_at` o `updated_at` son `None`, `to_dict()` retorne `None` sin fallar.
- [ ] **Método `User.create_table()`:** Validar que cree la tabla si no existe e informe adecuadamente si ya existe mediante el inspector de SQLAlchemy.

### 5.2 Pruebas de Integración de Restricciones de Base de Datos
- [ ] **Restricción de nulidad en `username`:** Inserción de `User` con `username=None` lanza error de integridad de BD.
- [ ] **Restricción de nulidad en `email`:** Inserción de `User` con `email=None` lanza error de integridad de BD.
- [ ] **Restricción de nulidad en `password`:** Inserción de `User` con `password=None` lanza error de integridad de BD.
- [ ] **Restricción de unicidad en `username`:** Inserción directa de dos usuarios con el mismo `username` viola restricción `UNIQUE`.
- [ ] **Restricción de unicidad en `email`:** Inserción directa de dos usuarios con el mismo `email` viola restricción `UNIQUE`.

---

## 6. Jerarquía de Excepciones de Dominio (`src/services/exceptions.py`)

Pruebas unitarias para validar las clases de error personalizadas y sus códigos por defecto.

- [ ] **`AppError` base:** Validar atributos `message`, `code` y `details` (diccionario por defecto).
- [ ] **`ValidationError`:** Validar herencia de `AppError` y código por defecto `'VALIDATION_ERROR'`.
- [ ] **`ConflictError`:** Validar herencia de `AppError` y código por defecto `'CONFLICT'`.
- [ ] **`DatabaseError`:** Validar herencia de `AppError` y código por defecto `'DB_ERROR'`.
- [ ] **`NotFoundError`:** Validar herencia de `AppError` y código por defecto `'NOT_FOUND'`.

---

## 7. Configuración y Conectividad MySQL (`src/config/mysql_config.py`)

Pruebas sobre la configuración de conexión y función de verificación ping.

- [ ] **Construcción de URI de conexión:** Validar que `Config.SQLALCHEMY_DATABASE_URI` ensamble correctamente el formato `mysql+pymysql://<user>:<pass>@<host>:<port>/<db>`.
- [ ] **Lectura de variables de entorno:** Validar valores por defecto y sobreescritura desde `.env`.
- [ ] **Función `verify_database_connection` (Éxito):** Mockear `create_engine` para simular respuesta exitosa de `SELECT 1` y validar que retorne `True`.
- [ ] **Función `verify_database_connection` (Fallo):** Mockear `create_engine` lanzando excepción y validar que capture el error y retorne `False`.

---

## 8. Matriz Consolidada de Pruebas

| Módulo / Componente | Tipo de Prueba | Pruebas Implementadas `[x]` | Pruebas Pendientes `[ ]` | Total Identificadas | Estado de Cobertura Actual |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Health Check (`/health`)** | Unitaria / Integración | 5 | 3 | 8 | 100% de líneas de `health.py` cubiertas |
| **Enrutamiento y App (`app.py`)** | Integración | 2 | 3 | 5 | 74% de líneas cubiertas |
| **Usuarios: Listar (`GET /users`)** | Integración / Unitaria | 2 | 3 | 5 | Parcialmente cubierto |
| **Usuarios: Crear (`POST /users`)** | Integración / Unitaria | 1 | 11 | 12 | Flujo exitoso cubierto; validaciones pendientes |
| **Usuarios: Actualizar (`PUT /users/<id>`)** | Integración / Unitaria | 1 | 11 | 12 | Flujo exitoso cubierto; validaciones pendientes |
| **Usuarios: Consultar ID (`GET /users/<id>`)** | Unitaria (Mock) / Integración | 1 | 4 | 5 | Mock cubierto; lógica real y BD pendiente |
| **Usuarios: Eliminar (`DELETE /users/<id>`)** | Unitaria (Mock) / Integración | 1 | 5 | 6 | Mock cubierto; lógica real y BD pendiente |
| **Servicio de Usuarios (`UserService`)** | Unitaria (Mocks) | 0 | 14 | 14 | No existen pruebas unitarias puras del servicio |
| **Modelo ORM (`User`)** | Unitaria / Integración | 0 | 10 | 10 | Cubierto indirectamente por integración |
| **Excepciones (`exceptions.py`)** | Unitaria | 0 | 5 | 5 | Instanciación probada solo en flujos |
| **Configuración MySQL (`mysql_config.py`)** | Unitaria | 0 | 4 | 4 | 57% de líneas cubiertas |
| **TOTALES** | | **13** | **49** | **62** | **69% Cobertura Global** |

---

## 9. Comandos para Ejecución y Verificación

Para ejecutar la suite de pruebas actual y verificar el estado y cobertura:

```bash
# 1. Activar el entorno virtual
source venv/bin/activate

# 2. Ejecutar todas las pruebas en modo detallado
pytest -v

# 3. Ejecutar pruebas con reporte de cobertura en terminal mostrando líneas faltantes
pytest --cov=src --cov-report=term-missing

# 4. Generar reporte HTML interactivo
pytest --cov=src --cov-report=html

# 5. Abrir reporte HTML en navegador (Linux)
xdg-open htmlcov/index.html
```
