CREATE TABLE Categorias (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255)
);
CREATE TABLE Roles (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255)
);
CREATE TABLE Plantas (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255),
    Descripcion TEXT,
    Precio DECIMAL(10, 2),
    categoria_id INT,
    Imagen VARCHAR(255),
    FOREIGN KEY (categoria_id) REFERENCES Categorias(ID)
);

CREATE TABLE Inventario (
    ID SERIAL PRIMARY KEY,
    id_planta INT,
    Cantidad INT,
    Ubicacion VARCHAR(255),
    FOREIGN KEY (id_planta) REFERENCES Plantas(ID)
);

CREATE TABLE Publicaciones (
    ID SERIAL PRIMARY KEY,
    Titulo VARCHAR(255),
    Contenido TEXT,
    Fecha DATE,
    id_planta INT,
    FOREIGN KEY (id_planta) REFERENCES Plantas(ID)
);

CREATE TABLE Usuarios (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255),
    Estado VARCHAR(20) DEFAULT 'Pendiente', 
	id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES Roles(ID)
);

CREATE TABLE Comentarios (
    ID SERIAL PRIMARY KEY,
    Comentario TEXT,
    Fecha DATE,
    Autor VARCHAR(255),
	id_publicacion INT,
    FOREIGN KEY (id_publicacion) REFERENCES Publicaciones(ID)
);


