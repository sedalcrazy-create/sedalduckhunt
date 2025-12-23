-- DuckHunt Challenge Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    bale_user_id TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employee_code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER DEFAULT 0,
    ducks_shot INTEGER DEFAULT 0,
    accuracy INTEGER DEFAULT 0,
    game_duration INTEGER DEFAULT 0,
    level_reached INTEGER DEFAULT 1,
    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_leaderboard_user_id ON leaderboard(user_id);
CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboard(score DESC);
CREATE INDEX IF NOT EXISTS idx_users_bale_id ON users(bale_user_id);

-- High scores view
CREATE OR REPLACE VIEW high_scores AS
SELECT
    u.id,
    u.bale_user_id,
    u.first_name,
    u.last_name,
    u.employee_code,
    COALESCE(MAX(l.score), 0) as high_score,
    COALESCE(MAX(l.ducks_shot), 0) as max_ducks,
    COALESCE(MAX(l.level_reached), 0) as max_level,
    COUNT(l.id) as games_played,
    MAX(l.game_date) as last_played
FROM users u
LEFT JOIN leaderboard l ON u.id = l.user_id
GROUP BY u.id, u.bale_user_id, u.first_name, u.last_name, u.employee_code
ORDER BY high_score DESC, max_ducks DESC;
