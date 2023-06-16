CREATE DATABASE IF NOT EXISTS midnight;
USE midnight;

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    ip TEXT NOT NULL  
);

CREATE TABLE IF NOT EXISTS exploits (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    threads INTEGER NOT NULL,
    timeout INTEGER NOT NULL,
    running INTEGER DEFAULT 0,
    source TEXT
);

CREATE TABLE IF NOT EXISTS exploit_teams (
    exploit_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    PRIMARY KEY(exploit_id, team_id),
    FOREIGN KEY(exploit_id) REFERENCES exploits(id) ON DELETE CASCADE,
    FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    exploit_id INTEGER,
    team_id INTEGER,
    time INTEGER(11) NOT NULL,
    exitcode INTEGER,
    FOREIGN KEY(exploit_id) REFERENCES exploits(id) ON DELETE SET NULL,
    FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS flags (
    flag VARCHAR(32) PRIMARY KEY,
    run_id INTEGER NOT NULL,
    status INTEGER NOT NULL,
    checksystem_response TEXT,
    FOREIGN KEY(run_id) REFERENCES runs(id)    
);

-- CREATE INDEX IF NOT EXISTS flags_sploit ON flags(sploit);
-- CREATE INDEX IF NOT EXISTS flags_team ON flags(team);
-- CREATE INDEX IF NOT EXISTS flags_status_time ON flags(status, time);
-- CREATE INDEX IF NOT EXISTS flags_time ON flags(time);
