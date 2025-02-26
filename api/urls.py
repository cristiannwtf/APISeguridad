from django.urls import path
from api.views import ReportePagosPorEmpleadoView, ReportePagosPorEmpleadoPDFView, EmpleadosListView, PagosListView

# Define las rutas URL para la aplicación 'api'.
urlpatterns = [
    # Ruta para obtener el reporte de pagos de un empleado en formato CSV.
    path('api/reportes/pagos/empleado/<int:empleado_id>/', ReportePagosPorEmpleadoView.as_view(), name='reporte_pagos_empleado'),
    
    # Ruta para obtener el reporte de pagos de un empleado en formato PDF.
    path('api/reportes/pagos/empleado/<int:empleado_id>/pdf/', ReportePagosPorEmpleadoPDFView.as_view(), name='reporte_pagos_empleado_pdf'),

    # Nueva ruta para obtener la lista de empleados.
    path('api/empleados/', EmpleadosListView.as_view(), name='empleados_list'),

    # Nueva ruta para obtener la lista de pagos.
    path('api/pagos/', PagosListView.as_view(), name='pagos_list'),
]
