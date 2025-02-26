# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.db import connection
import csv

# Importaciones necesarias para generar PDFs
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ReportePagosPorEmpleadoView(APIView):
    # Clases de autenticación y permisos para la vista
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, empleado_id):
        try:
            # Obtener el ID del usuario autenticado
            usuario_id = request.user.id

            # Ejecutar procedimientos almacenados en la base de datos
            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_set_session_context 'UsuarioID', %s;", [usuario_id])
                cursor.execute("EXEC sp_ReportePagosPorEmpleado @EmpleadoID=%s;", [empleado_id])
                columns = [col[0] for col in cursor.description]
                pagos = [dict(zip(columns, row)) for row in cursor.fetchall()]

                # Si no hay pagos, devolver una respuesta adecuada
                if not pagos:
                    return HttpResponseNotFound(f"No se encontraron pagos para el EmpleadoID {empleado_id}.")

                # Registrar el reporte generado
                cursor.execute("""
                    INSERT INTO ReportesGenerados (UsuarioID, TipoReporte, Parametros)
                    VALUES (%s, %s, %s);
                """, [usuario_id, 'PorEmpleado', f'EmpleadoID={empleado_id}'])

            # Generar CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="reporte_pagos_empleado_{empleado_id}.csv"'
            response.write('\ufeff'.encode('utf8'))  # Añadir BOM para Unicode

            writer = csv.DictWriter(response, fieldnames=columns)
            writer.writeheader()
            for pago in pagos:
                writer.writerow(pago)

            return response

        except Exception as e:
            # Manejo de errores
            print(f"Error al generar el reporte para EmpleadoID {empleado_id}: {e}")
            return HttpResponseServerError("Se produjo un error al generar el reporte.")

class ReportePagosPorEmpleadoPDFView(APIView):
    # Clases de autenticación y permisos para la vista
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, empleado_id):
        try:
            # Agregar líneas de depuración
            print(f"Usuario autenticado: {request.user.is_authenticated}")
            print(f"Usuario: {request.user}")
            print(f"Usuario ID: {request.user.id}")

            # Obtener el ID del usuario autenticado
            usuario_id = request.user.id

            # Ejecutar procedimientos almacenados en la base de datos
            with connection.cursor() as cursor:
                cursor.execute("EXEC sp_set_session_context 'UsuarioID', %s;", [usuario_id])
                cursor.execute("EXEC sp_ReportePagosPorEmpleado @EmpleadoID=%s;", [empleado_id])
                pagos = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

                # Si no hay pagos, devolver una respuesta adecuada
                if not pagos:
                    return HttpResponseNotFound(f"No se encontraron pagos para el EmpleadoID {empleado_id}.")

                # Registrar el reporte generado
                cursor.execute("""
                    INSERT INTO ReportesGenerados (UsuarioID, TipoReporte, Parametros)
                    VALUES (%s, %s, %s);
                """, [usuario_id, 'PorEmpleadoPDF', f'EmpleadoID={empleado_id}'])

            # Generar PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="reporte_pagos_empleado_{empleado_id}.pdf"'

            c = canvas.Canvas(response, pagesize=letter)
            width, height = letter

            # Título
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"Reporte de Pagos - Empleado {empleado_id}")

            # Encabezados de columna
            c.setFont("Helvetica-Bold", 12)
            y_position = height - 80
            for index, column in enumerate(columns):
                c.drawString(50 + index * 100, y_position, str(column))

            # Datos
            c.setFont("Helvetica", 10)
            y_position -= 20
            for pago in pagos:
                for index, value in enumerate(pago):
                    c.drawString(50 + index * 100, y_position, str(value))
                y_position -= 20

                # Salto de página si es necesario
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50

            c.showPage()
            c.save()

            return response

        except Exception as e:
            # Manejo de errores
            print(f"Error al generar el reporte PDF para EmpleadoID {empleado_id}: {e}")
            return HttpResponseServerError("Se produjo un error al generar el reporte PDF.")
