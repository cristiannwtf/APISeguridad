-- functions.sql

-- Función para obtener el UsuarioID actual
CREATE FUNCTION dbo.fn_ObtenerUsuarioID()
RETURNS INT
AS
BEGIN
    DECLARE @UsuarioID INT;
    SET @UsuarioID = CONVERT(INT, SESSION_CONTEXT(N'UsuarioID'));
    RETURN @UsuarioID;
END;
