from django.apps import AppConfig

# Esta clase configura la aplicación 'api' dentro del proyecto Django.
# Hereda de AppConfig, que es la clase base para todas las configuraciones de aplicaciones en Django.
class ApiConfig(AppConfig):
    # Define el tipo de campo automático predeterminado para los modelos en esta aplicación.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Especifica el nombre de la aplicación. Este nombre debe coincidir con el nombre del directorio de la aplicación.
    name = 'api'
