CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(3)
);

INSERT INTO users (username, password) VALUES
('tomek', 'A12'),
('marek', 'B34'),
('darek', 'C56'),
('mariusz', 'D78'),
('krystian', 'E90'),
('bartek', 'F12'),
('sebastian', 'G34'),
('szymon', 'H56'),
('ignacy', 'I78'),
('borys', 'J90');