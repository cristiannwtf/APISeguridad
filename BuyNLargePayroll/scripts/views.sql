-- views.sql

-- Vista para empleados con permisos
CREATE VIEW vw_EmpleadosConPermisos AS
SELECT DISTINCT e.*
FROM Empleados e
INNER JOIN UsuariosRoles ur ON ur.UsuarioID = dbo.fn_ObtenerUsuarioID()
INNER JOIN RolesPermisos rp ON rp.RolID = ur.RolID
INNER JOIN Permisos p ON p.PermisoID = rp.PermisoID
WHERE p.NombreObjeto = 'Empleados' AND p.Accion = 'SELECT' AND (
    p.FiltroTipo = 'FullAccess' -- Acceso total
    OR
    (p.FiltroTipo = 'PorUsuario' AND e.UsuarioID = dbo.fn_ObtenerUsuarioID())
    OR
    (p.FiltroTipo = 'PorDepartamento' AND e.DepartamentoID = (
       SELECT DepartamentoID FROM Departamentos WHERE UsuarioID = dbo.fn_ObtenerUsuarioID()
    ))
);

-- Vista para pagos con permisos
CREATE VIEW vw_PagosConPermisos AS
SELECT DISTINCT p.*
FROM Pagos p
INNER JOIN Empleados e ON p.EmpleadoID = e.EmpleadoID
INNER JOIN UsuariosRoles ur ON ur.UsuarioID = dbo.fn_ObtenerUsuarioID()
INNER JOIN RolesPermisos rp ON rp.RolID = ur.RolID
INNER JOIN Permisos per ON per.PermisoID = rp.PermisoID
WHERE per.NombreObjeto = 'Pagos' AND per.Accion = 'SELECT' AND (
    per.FiltroTipo = 'FullAccess' -- Acceso total
    OR
    (per.FiltroTipo = 'PorUsuario' AND e.UsuarioID = dbo.fn_ObtenerUsuarioID())
    OR
    (per.FiltroTipo = 'PorDepartamento' AND e.DepartamentoID = (
        SELECT DepartamentoID FROM Departamentos WHERE UsuarioID = dbo.fn_ObtenerUsuarioID()
    ))
);
