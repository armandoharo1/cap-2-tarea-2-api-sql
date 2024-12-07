-- Crear la tabla 'posts'
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar registros de ejemplo
INSERT INTO posts (title, content) VALUES 
('Primer Post', 'Este es el contenido del primer post.'),
('Segundo Post', 'Contenido del segundo post.'),
('Tercer Post', 'Más contenido interesante en el tercer post.');
