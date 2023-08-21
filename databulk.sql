-- Datos de prueba para la tabla "Categorias"
INSERT INTO Categorias (Nombre) VALUES
    ('Flores'),
    ('Árboles'),
    ('Suculentas'),
    ('Hierbas');

-- Datos de prueba para la tabla "Roles"
INSERT INTO Roles (Nombre) VALUES
    ('Admin'),
    ('Usuario');

-- Datos de prueba para la tabla "Plantas"
INSERT INTO Plantas (Nombre, Descripcion, Precio, categoria_id, Imagen) VALUES
    ('Rosa', 'Hermosa flor de jardín', 12.99, 1, 'https://ejemplo.com/rosa.jpg'),
    ('Roble', 'Árbol de hoja perenne', 89.99, 2, 'https://ejemplo.com/roble.jpg'),
    ('Echeveria', 'Pequeña planta suculenta', 6.50, 3, 'https://ejemplo.com/echeveria.jpg');

-- Datos de prueba para la tabla "Usuarios"
INSERT INTO Usuarios (Nombre, id_rol) VALUES
    ('admin', 1),
    ('usuario1', 2),
    ('usuario2', 2);

-- Datos de prueba para la tabla "Publicaciones"
INSERT INTO Publicaciones (Titulo, Contenido, Fecha, id_planta) VALUES
    ('Nueva Rosa en el Jardín', 'Hemos añadido una hermosa rosa a nuestro jardín', '2023-08-15', 1),
    ('Descubriendo el Mundo de las Suculentas', 'Explorando las distintas variedades de suculentas', '2023-08-16', 3);

-- Datos de prueba para la tabla "Comentarios"
INSERT INTO Comentarios (Comentario, Fecha, Autor, id_publicacion) VALUES
    ('¡Qué hermosa rosa!', '2023-08-15', 'usuario1', 1),
    ('Me encantan las suculentas', '2023-08-16', 'usuario2', 2);
