PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    company TEXT,
    industry TEXT,
    seniority TEXT,
    summary TEXT,
    style TEXT,
    raw_profile TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prospect_id) REFERENCES prospects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_prospects_industry ON prospects(industry);
CREATE INDEX IF NOT EXISTS idx_prospects_role ON prospects(role);
CREATE INDEX IF NOT EXISTS idx_messages_channel ON messages(channel);

