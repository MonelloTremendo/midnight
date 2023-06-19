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
    runperiod INTEGER NOT NULL,
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
    start_time INTEGER(11) NOT NULL,
    end_time INTEGER(11) NOT NULL,
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


CREATE INDEX flags_status ON flags(status);
CREATE INDEX flags_run ON flags(run_id);

CREATE INDEX runs_end_time ON runs(end_time);


INSERT INTO `teams` VALUES (1,'test','10.60.69.1');
INSERT INTO `exploits` VALUES (1,'testExploit',16,60,10,'IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoKaW1wb3J0IHJhbmRvbQppbXBvcnQgc3RyaW5nCgpmb3IgXyBpbiByYW5nZSgxMCk6CiAgICBwcmludCgiIi5qb2luKHJhbmRvbS5jaG9pY2Uoc3RyaW5nLmFzY2lpX3VwcGVyY2FzZSkgZm9yIF8gaW4gcmFuZ2UoMzEpKSArICI9IiwgZmx1c2g9VHJ1ZSk=');

INSERT INTO `exploit_teams` VALUES (1,1);
