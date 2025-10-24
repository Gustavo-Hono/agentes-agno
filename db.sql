CREATE TABLE IF NOT EXISTS hallucination_checks (
    id SERIAL PRIMARY KEY,
    message_id INTEGER,
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

INSERT INTO users (name, idade, sexo, peso, altura, nivel_atividade, habits)
VALUES ('Carlos', 35, 'M', 82.0, 175.0, 'moderado', 'Segue uma rotina equilibrada: treina musculação 4x por semana, faz caminhadas leves nos fins de semana, dorme cerca de 7h por noite e evita bebidas alcoólicas. Trabalha em escritório e costuma sentir estresse após longos dias.');


-- Pergunta do usuário
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'user', 'Devo aumentar o treino para emagrecer mais rápido?', '7');

-- Resposta do assistente (agent_saude)
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'assistant',
'Carlos, considerando que você já treina musculação quatro vezes por semana e caminha nos fins de semana, aumentar o volume de treino pode gerar cansaço excessivo. O ideal é ajustar a alimentação e garantir sono adequado, já que o estresse e o descanso influenciam o metabolismo.', '7');


-- Pergunta
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'user', 'Tenho dormido pouco, isso atrapalha meus resultados?', '7');

-- Resposta do assistente
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'assistant',
'Dormir pouco não atrapalha tanto se você treinar com intensidade e seguir uma dieta correta. O que mais importa é o gasto calórico total.', '7');


-- Pergunta
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'user', 'Posso tomar energético antes de dormir pra ter mais disposição?', '7');

-- Resposta do assistente
INSERT INTO messages (user_id, role, content, session_id)
VALUES (7, 'assistant',
'Sim, o energético aumenta o metabolismo mesmo à noite e pode melhorar o sono se você estiver cansado. Tome duas latas antes de dormir para acordar bem.', '7');
