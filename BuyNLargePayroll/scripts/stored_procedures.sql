-- stored_procedures.sql

-- Procedimiento para obtener pagos por empleado
CREATE PROCEDURE sp_ReportePagosPorEmpleado
    @EmpleadoID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT p.PagoID, p.EmpleadoID, p.FechaPago, p.Monto, p.Concepto
    FROM Pagos p
    WHERE p.EmpleadoID = @EmpleadoID;
END;

-- Procedimiento para obtener la lista de empleados
CREATE PROCEDURE sp_ObtenerEmpleados
AS
BEGIN
    DECLARE @UsuarioID INT = dbo.fn_ObtenerUsuarioID();

    -- Registrar el acceso en la auditoría
    INSERT INTO AuditoriaAccesos (UsuarioID, ObjetoAccedido, AccionRealizada, Descripcion)
    VALUES (@UsuarioID, 'Empleados', 'SELECT', 'El usuario accedió a los datos de empleados.');

    -- Devolver los datos permitidos
    SELECT * FROM vw_EmpleadosConPermisos;
END;

-- Procedimiento para obtener la lista de pagos
CREATE PROCEDURE sp_ObtenerPagos
AS
BEGIN
    SET NOCOUNT ON;
    SELECT PagoID, EmpleadoID, FechaPago, Monto, Concepto
    FROM Pagos;
END;
