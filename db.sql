CREATE TABLE IF NOT EXISTS hallucination_checks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    veredict JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);