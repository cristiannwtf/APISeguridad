from django.contrib import admin
from django.urls import path, include

# Define las rutas URL para el proyecto 'BuyNLargePayroll'.
urlpatterns = [
    # Ruta para acceder al sitio de administración de Django.
    path('admin/', admin.site.urls),
    
    # Incluye las rutas definidas en la aplicación 'api'.
    path('', include('api.urls')),
]
