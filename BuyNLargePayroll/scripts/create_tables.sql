-- create_tables.sql

-- Tabla Usuarios
CREATE TABLE Usuarios (
    UsuarioID INT IDENTITY(1,1) PRIMARY KEY,
    NombreUsuario VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Contraseña VARCHAR(255) NOT NULL, -- Debe almacenarse encriptada (hash)
    Activo BIT NOT NULL DEFAULT 1
);

-- Tabla Roles
CREATE TABLE Roles (
    RolID INT IDENTITY(1,1) PRIMARY KEY,
    NombreRol VARCHAR(50) NOT NULL UNIQUE,
    Descripcion VARCHAR(255) NULL
);

-- Tabla UsuariosRoles (Relación muchos a muchos entre Usuarios y Roles)
CREATE TABLE UsuariosRoles (
    UsuarioID INT NOT NULL,
    RolID INT NOT NULL,
    PRIMARY KEY (UsuarioID, RolID),
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID),
    FOREIGN KEY (RolID) REFERENCES Roles(RolID)
);

-- Tabla Permisos
CREATE TABLE Permisos (
    PermisoID INT IDENTITY(1,1) PRIMARY KEY,
    TipoObjeto VARCHAR(20) NOT NULL,       -- 'Tabla' o 'Registro'
    NombreObjeto VARCHAR(100) NOT NULL,    -- Nombre de la tabla o identificación del objeto
    Accion VARCHAR(10) NOT NULL,           -- 'SELECT', 'INSERT', 'UPDATE', 'DELETE'
    Filtro VARCHAR(1000) NULL              -- Condición para registros específicos (opcional)
);

-- Tabla RolesPermisos (Relación muchos a muchos entre Roles y Permisos)
CREATE TABLE RolesPermisos (
    RolID INT NOT NULL,
    PermisoID INT NOT NULL,
    PRIMARY KEY (RolID, PermisoID),
    FOREIGN KEY (RolID) REFERENCES Roles(RolID),
    FOREIGN KEY (PermisoID) REFERENCES Permisos(PermisoID)
);

-- Tabla UsuariosPermisos (Permisos asignados directamente a usuarios)
CREATE TABLE UsuariosPermisos (
    UsuarioID INT NOT NULL,
    PermisoID INT NOT NULL,
    PRIMARY KEY (UsuarioID, PermisoID),
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID),
    FOREIGN KEY (PermisoID) REFERENCES Permisos(PermisoID)
);

-- Tabla Departamentos
CREATE TABLE Departamentos (
    DepartamentoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreDepartamento VARCHAR(100) NOT NULL UNIQUE,
    Ubicacion VARCHAR(100) NULL,
    UsuarioID INT NULL,  -- Nuevo campo para relacionar con Usuarios (opcional)
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);

-- Tabla Empleados
CREATE TABLE Empleados (
    EmpleadoID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Telefono VARCHAR(20) NULL,
    Direccion VARCHAR(255) NULL,
    DepartamentoID INT NOT NULL,
    UsuarioID INT NULL,  -- Nuevo campo para relacionar con Usuarios
    FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(DepartamentoID),
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);

-- Tabla Pagos
CREATE TABLE Pagos (
    PagoID INT IDENTITY(1,1) PRIMARY KEY,
    EmpleadoID INT NOT NULL,
    FechaPago DATE NOT NULL,
    Monto DECIMAL(18,2) NOT NULL,
    Concepto VARCHAR(255) NULL,
    FOREIGN KEY (EmpleadoID) REFERENCES Empleados(EmpleadoID)
);

-- Tabla AuditoriaAccesos
CREATE TABLE AuditoriaAccesos (
    AuditoriaID INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioID INT NOT NULL,
    FechaHoraAcceso DATETIME NOT NULL DEFAULT GETDATE(),
    ObjetoAccedido VARCHAR(100) NOT NULL,
    AccionRealizada VARCHAR(10) NOT NULL,
    Descripcion VARCHAR(255) NULL,
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);

-- Tabla ReportesGenerados
CREATE TABLE ReportesGenerados (
    ReporteID INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioID INT NOT NULL,
    TipoReporte VARCHAR(50) NOT NULL,    -- 'PorEmpleado', 'PorDepartamento', 'PorPeriodo'
    Parametros VARCHAR(500) NULL,        -- Información sobre los parámetros usados
    FechaHoraGeneracion DATETIME NOT NULL DEFAULT GETDATE(),
    RutaArchivo VARCHAR(255) NULL,       -- Ubicación del archivo CSV o PDF generado
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);
