CREATE TABLE filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    ano INTEGER,
    genero TEXT,
    sinopse TEXT
);
INSERT INTO filmes (titulo, ano, genero, sinopse)
VALUES
('Interestelar', 2014, 'Ficção científica', 'Uma equipe de astronautas parte em uma missão pelo espaço em busca de um novo lar para a humanidade.'),
('O Poderoso Chefão', 1972, 'Crime', 'A história da família Corleone e seu envolvimento com o crime organizado.');