# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.db import connection
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Empleado, Pago

# Vista para generar un reporte de pagos por empleado en formato CSV
class ReportePagosPorEmpleadoView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, empleado_id):
        try:
            # Obtener el UsuarioID de SQL Server
            usuario_id_sql = request.user.usuario_id_sql
            if not usuario_id_sql:
                return HttpResponseServerError("El usuario no tiene asociado un UsuarioID de SQL Server.")

            with connection.cursor() as cursor:
                # Ejecutar el procedimiento almacenado para obtener los pagos del empleado
                cursor.execute("EXEC sp_ObtenerPagosPorEmpleado @UsuarioID=%s, @EmpleadoID=%s;", [usuario_id_sql, empleado_id])
                columns = [col[0] for col in cursor.description]
                pagos = [dict(zip(columns, row)) for row in cursor.fetchall()]

                # Verificar si se encontraron pagos
                if not pagos:
                    return HttpResponseNotFound(f"No se encontraron pagos para el EmpleadoID {empleado_id}.")

            # Generar la respuesta en formato CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="reporte_pagos_empleado_{empleado_id}.csv"'
            writer = csv.DictWriter(response, fieldnames=columns)
            writer.writeheader()
            for pago in pagos:
                writer.writerow(pago)

            return response

        except Exception as e:
            print(f"Error al generar el reporte CSV para EmpleadoID {empleado_id}: {e}")
            return HttpResponseServerError("Se produjo un error al generar el reporte CSV.")

# Vista para generar un reporte de pagos por empleado en formato PDF
class ReportePagosPorEmpleadoPDFView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, empleado_id):
        try:
            # Obtener el UsuarioID de SQL Server
            usuario_id_sql = request.user.usuario_id_sql
            if not usuario_id_sql:
                return HttpResponseServerError("El usuario no tiene asociado un UsuarioID de SQL Server.")

            with connection.cursor() as cursor:
                # Ejecutar el procedimiento almacenado para obtener los pagos del empleado
                cursor.execute("EXEC sp_ObtenerPagosPorEmpleado @UsuarioID=%s, @EmpleadoID=%s;", [usuario_id_sql, empleado_id])
                pagos = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

                # Verificar si se encontraron pagos
                if not pagos:
                    return HttpResponseNotFound(f"No se encontraron pagos para el EmpleadoID {empleado_id}.")

            # Generar la respuesta en formato PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte_pagos_empleado_{empleado_id}.pdf"'

            c = canvas.Canvas(response, pagesize=letter)
            width, height = letter

            # Título del reporte
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"Reporte de Pagos - Empleado {empleado_id}")

            # Encabezados de las columnas
            c.setFont("Helvetica-Bold", 12)
            y_position = height - 80
            for index, column in enumerate(columns):
                c.drawString(50 + index * 100, y_position, str(column))

            # Datos de los pagos
            c.setFont("Helvetica", 10)
            y_position -= 20
            for pago in pagos:
                for index, value in enumerate(pago):
                    c.drawString(50 + index * 100, y_position, str(value))
                y_position -= 20

                # Nueva página si es necesario
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50

            c.save()

            return response

        except Exception as e:
            print(f"Error al generar el reporte PDF para EmpleadoID {empleado_id}: {e}")
            return HttpResponseServerError("Se produjo un error al generar el reporte PDF.")

# Vista para obtener la lista de empleados con permisos
class EmpleadosListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            usuario_id_sql = request.user.usuario_id_sql
            if not usuario_id_sql:
                return HttpResponseServerError("El usuario no tiene asociado un UsuarioID de SQL Server.")

            print(f"Usuario ID SQL: {usuario_id_sql}")

            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_ObtenerEmpleados @UsuarioID=%s;", [usuario_id_sql])

                if cursor.description is None:
                    print("La consulta no devolvió resultados.")
                    return HttpResponseServerError("Se produjo un error al obtener la lista de empleados.")

                columns = [col[0] for col in cursor.description]
                empleados = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return JsonResponse(empleados, safe=False)

        except Exception as e:
            import traceback
            traceback.print_exc()  # Esto imprimirá el traceback completo en la consola
            return HttpResponseServerError(f"Se produjo un error al obtener la lista de empleados: {e}")

# Vista para obtener la lista de pagos con permisos
class PagosListView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            usuario_id_sql = request.user.usuario_id_sql
            if not usuario_id_sql:
                return HttpResponseServerError("El usuario no tiene asociado un UsuarioID de SQL Server.")

            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_ObtenerPagos @UsuarioID=%s;", [usuario_id_sql])
                columns = [col[0] for col in cursor.description]
                pagos = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return JsonResponse(pagos, safe=False)

        except Exception as e:
            import traceback
            traceback.print_exc()  # Esto imprimirá el traceback completo en la consola
            return HttpResponseServerError(f"Se produjo un error al obtener la lista de pagos: {e}")
