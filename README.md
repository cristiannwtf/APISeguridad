# APISeguridad

## Descripción

**APISeguridad** es un sistema de control de permisos granular para una API desarrollado para **Buy n Large**. El proyecto implementa un software de nómina donde los usuarios tienen acceso restringido a nivel de tabla y registro según su rol o usuario, con la lógica de permisos implementada en SQL Server.

## Instalación

### Requisitos Previos

- Python 3.x
- SQL Server
- pip

### Pasos de Instalación

1. **Clonar este repositorio:**

    ```bash
    git clone https://github.com/cristiannwtf/APISeguridad.git
    ```

2. **Navegar al directorio del proyecto:**

    ```bash
    cd APISeguridad
    ```

3. **Crear y activar un entorno virtual (recomendado):**

    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

4. **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configurar la base de datos:**

    - Ejecuta los scripts SQL en la carpeta `scripts/` en tu instancia de SQL Server para crear las tablas y procedimientos almacenados.
    - Configura la conexión a la base de datos en `BuyNLargePayroll/settings.py`.

6. **Realizar las migraciones de Django:**

    ```bash
    python manage.py migrate
    ```

7. **Crear un superusuario:**

    ```bash
    python manage.py createsuperuser
    ```

8. **Ejecutar el servidor de desarrollo:**

    ```bash
    python manage.py runserver
    ```

## Uso de la Aplicación

- **Endpoints disponibles:**

  - Obtener empleados: `/api/empleados/`
  - Generar reporte en CSV: `/api/reportes/pagos/empleado/<int:empleado_id>/`
  - Generar reporte en PDF: `/api/reportes/pagos/empleado/<int:empleado_id>/pdf/`

- **Autenticación:**

  Los endpoints requieren autenticación básica. Usa las credenciales del superusuario que creaste.

- **Ejemplo de solicitud con `curl`:**

    ```bash
    curl -u admin:contraseña http://localhost:8000/api/reportes/pagos/empleado/1/
    ```

## Características Implementadas

- **Sistema de permisos granular** en SQL Server.
- **Generación de reportes de nómina** en formatos CSV y PDF.
- **Auditoría de accesos** para registrar quién accede a información sensible y cuándo.

## Estructura del Proyecto

```plaintext
APISeguridad/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── BuyNLargePayroll/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── scripts/
│   ├── create_tables.sql
│   ├── stored_procedures.sql
│   └── data.sql
├── manage.py
├── requirements.txt
└── README.md
