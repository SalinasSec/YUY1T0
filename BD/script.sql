DROP DATABASE IF EXISTS clinica;
CREATE DATABASE clinica;
USE clinica;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    rol ENUM('usuario','admin') DEFAULT 'usuario'
);

-- Tabla de turnos
CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente','aceptado','rechazado','atendido','cancelado') DEFAULT 'pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Crear admin por defecto
INSERT INTO usuarios (nombre, email, password, rol)
VALUES ('Admin', 'admin@clinica.com', 'admin123', 'admin');

SELECT * FROM usuarios;