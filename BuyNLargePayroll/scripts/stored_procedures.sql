-- stored_procedures.sql

-- Procedimiento para obtener pagos por empleado
CREATE PROCEDURE sp_ReportePagosPorEmpleado
    @UsuarioID INT,
    @EmpleadoID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Obtener el DepartamentoID del usuario
    DECLARE @DepartamentoID INT;
    SELECT @DepartamentoID = DepartamentoID FROM Empleados WHERE UsuarioID = @UsuarioID;

    -- Verificar los permisos y filtrar los pagos
    SELECT p.*
    FROM Pagos p
    INNER JOIN Empleados e ON p.EmpleadoID = e.EmpleadoID
    WHERE
        e.EmpleadoID = @EmpleadoID AND
        (
            -- El usuario tiene acceso si es administrador (FullAccess)
            EXISTS (
                SELECT 1
                FROM UsuariosRoles ur
                INNER JOIN RolesPermisos rp ON ur.RolID = rp.RolID
                INNER JOIN Permisos perm ON rp.PermisoID = perm.PermisoID
                WHERE ur.UsuarioID = @UsuarioID
                  AND perm.NombreObjeto = 'Pagos'
                  AND perm.Accion = 'SELECT'
                  AND perm.FiltroTipo = 'FullAccess'
            )
            -- O si es el propio usuario
            OR e.UsuarioID = @UsuarioID
            -- O si está en el mismo departamento
            OR e.DepartamentoID = @DepartamentoID
        );
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
    DECLARE @UsuarioID INT = dbo.fn_ObtenerUsuarioID();

    -- Registrar el acceso en la auditoría
    INSERT INTO AuditoriaAccesos (UsuarioID, ObjetoAccedido, AccionRealizada, Descripcion)
    VALUES (@UsuarioID, 'Pagos', 'SELECT', 'El usuario accedió a los datos de pagos.');

    -- Devolver los datos permitidos
    SELECT * FROM vw_PagosConPermisos;
END;
