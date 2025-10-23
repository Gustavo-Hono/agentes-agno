CREATE TABLE IF NOT EXISTS hallucination_checks (
    id SERIAL PRIMARY KEY,
    message_id INTEGER
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    veredict JSONB NOT NULL,
    justification TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    role TEXT CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    session_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    idade INT,
    sexo CHAR(1),
    peso DECIMAL(5,2),
    altura DECIMAL(5,2),
    nivel_atividade VARCHAR(20),
    habits TEXT
);

INSERT INTO users (name, idade, habits) VALUES
('Gustavo', 19, 'Segue uma dieta equilibrada com arroz, frango e legumes. Treina musculação 4x por semana e faz 2 sessões de cardio nos dias de treino. Dorme cerca de 7h por noite.'),
('Ana', 25, 'É vegetariana. Consome frutas, leguminosas e cereais integrais. Pratica yoga 3x por semana e caminha todos os dias. Evita bebidas alcoólicas.'),
('Lucas', 32, 'Segue dieta flexível com foco em ganho de massa. Treina musculação 5x por semana. Faz acompanhamento nutricional mensal.'),
('Mariana', 28, 'Segue dieta com restrição de glúten e lactose. Faz pilates 2x por semana e corre aos sábados. Dorme 8h por noite.'),
('Rafael', 40, 'Tem rotina de alimentação balanceada, evita frituras. Joga futebol 2x na semana e pedala aos domingos. Toma café sem açúcar.');