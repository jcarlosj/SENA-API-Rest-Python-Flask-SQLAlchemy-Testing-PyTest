# Guía de Configuración de MySQL y Solución de Conexión

Esta guía documenta el flujo real y ordenado para configurar MySQL recién instalado (especialmente en Fedora, RHEL o CentOS con `mysqld.service`) y conectarlo exitosamente con la API Flask.

---

## 1. El Diagnóstico del Error

Al arrancar la aplicación por primera vez con `python -m src.app`, aparece este error:

```text
✖ Error al conectar con la base de datos MySQL: (pymysql.err.OperationalError) (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

### ¿Por qué ocurre?
1. **Contraseña temporal obligatoria:** En Fedora/RHEL, el instalador de MySQL genera una contraseña temporal para `root` y bloquea cualquier acceso sin ella (`using password: NO`).
2. **Bloqueo de operaciones (`ERROR 1820`):** MySQL no permite ejecutar ninguna consulta (ni siquiera `CREATE DATABASE`) hasta que la contraseña de `root` haya sido cambiada mediante `ALTER USER`.
3. **Falta la base de datos:** Aún no existe la base de datos `mi_api_flask_db`.

---

## 2. Flujo de Configuración Paso a Paso (Orden Correcto)

### Paso 1: Obtener la contraseña temporal generada
Ejecuta en tu terminal del sistema:

```bash
sudo grep 'temporary password' /var/log/mysqld.log
```

Verás una salida similar a:
```text
[Note] [MY-010454] [Server] A temporary password is generated for root@localhost: Gp.aA5G%qlAp
```
Copia esa contraseña temporal.

---

### Paso 2: Entrar a la consola de MySQL
Ejecuta:

```bash
mysql -u root -p
```
Cuando te solicite `Enter password:`, pega la contraseña temporal y presiona `Enter`.

---

### Paso 3: Cambiar OBLIGATORIAMENTE la contraseña de `root` (Primero que todo)

> [!WARNING]
> Si intentas crear una base de datos o usuario antes de este paso, MySQL arrojará:
> `ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.`

Ejecuta inmediatamente en la consola de MySQL (`mysql>`):

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MiPasswordSegura123*';
```

> [!NOTE]
> **Política de contraseñas de MySQL:** Debe contener al menos 8 caracteres, mayúsculas, minúsculas, números y al menos un carácter especial (ejemplo: `RootPass123*`).

---

### Paso 4: Crear la Base de Datos

Ahora que la contraseña de `root` está restablecida, ya puedes crear la base de datos:

```sql
CREATE DATABASE IF NOT EXISTS mi_api_flask_db;
```

---

### Paso 5: Elegir cómo conectar la aplicación

Elige una de las siguientes dos opciones:

#### Opción A: Crear un usuario dedicado (Recomendada por Seguridad)
> [!TIP]
> **Principio de Mínimo Privilegio:** Es la mejor práctica para producción. El usuario solo tiene acceso a `mi_api_flask_db` y ningún permiso global en el servidor MySQL.

Ejecuta en `mysql>`:
```sql
-- 1. Crear el usuario exclusivo para la aplicación
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'FlaskPass123*';

-- 2. Conceder permisos únicamente sobre la base de datos del proyecto
GRANT ALL PRIVILEGES ON mi_api_flask_db.* TO 'flask_user'@'localhost';

-- 3. Aplicar privilegios y salir
FLUSH PRIVILEGES;
EXIT;
```

*Valores a poner en tu `.env`:*
```env
DB_USER=flask_user
DB_PASSWORD=FlaskPass123*
```

---

#### Opción B: Usar directamente el usuario `root`
> [!NOTE]
> Opción rápida para desarrollo local. No requiere crear más usuarios en MySQL.

Simplemente aplica los privilegios y sal de MySQL:
```sql
FLUSH PRIVILEGES;
EXIT;
```

*Valores a poner en tu `.env`:*
```env
DB_USER=root
DB_PASSWORD=MiPasswordSegura123*   # La contraseña que configuraste en el Paso 3
```

---

### Paso 6: Configurar el archivo `.env`

Asegúrate de que tu archivo `.env` en la raíz de `BackEnd/` tenga las credenciales correctas según la opción que elegiste:

```env
FLASK_ENV=development
DB_USER=flask_user        # O root si elegiste la Opción B
DB_PASSWORD=FlaskPass123* # O la contraseña de root del Paso 3
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mi_api_flask_db
```

---

## 3. Verificación de la Conexión

Guarda el archivo `.env` y vuelve a iniciar el servidor desde la raíz:

```bash
python -m src.app
```

Verás la confirmación exitosa en verde en la terminal:

```text
✔ Conexión a la base de datos MySQL establecida con éxito.
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
