from django.urls import path
from api.views import ReportePagosPorEmpleadoView, ReportePagosPorEmpleadoPDFView

# Define las rutas URL para la aplicación 'api'.
urlpatterns = [
    # Ruta para obtener el reporte de pagos de un empleado en formato CSV.
    # La URL incluye el ID del empleado como un parámetro.
    path('api/reportes/pagos/empleado/<int:empleado_id>/', ReportePagosPorEmpleadoView.as_view(), name='reporte_pagos_empleado'),
    
    # Ruta para obtener el reporte de pagos de un empleado en formato PDF.
    # La URL incluye el ID del empleado como un parámetro.
    path('api/reportes/pagos/empleado/<int:empleado_id>/pdf/', ReportePagosPorEmpleadoPDFView.as_view(), name='reporte_pagos_empleado_pdf'),
]
