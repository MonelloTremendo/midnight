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


INSERT INTO teams (ip, name) VALUE ("10.60.0.1", "TEAM_NOP");
INSERT INTO teams (ip, name) VALUE ("10.60.1.1", "Accademia Aeronautica di Pozzuoli");
INSERT INTO teams (ip, name) VALUE ("10.60.2.1", "Alma Mater Studiorum - Universita' di Bologna");
INSERT INTO teams (ip, name) VALUE ("10.60.3.1", "Centro di Competenza in Cybersecurity Toscano");
INSERT INTO teams (ip, name) VALUE ("10.60.4.1", "Comando per la Formazione e Scuola di Applicazione dell'Esercito");
INSERT INTO teams (ip, name) VALUE ("10.60.5.1", "Libera Universita' di Bolzano");
INSERT INTO teams (ip, name) VALUE ("10.60.6.1", "Politecnico di Bari");
INSERT INTO teams (ip, name) VALUE ("10.60.7.1", "Politecnico di Milano");
INSERT INTO teams (ip, name) VALUE ("10.60.8.1", "Politecnico di Torino");
INSERT INTO teams (ip, name) VALUE ("10.60.9.1", "Sapienza Universita' di Roma");
INSERT INTO teams (ip, name) VALUE ("10.60.10.1", "Universita' Ca' Foscari Venezia");
INSERT INTO teams (ip, name) VALUE ("10.60.11.1", "Universita' Campus Bio-Medico di Roma");
INSERT INTO teams (ip, name) VALUE ("10.60.12.1", "Universita' degli Studi della Campania Luigi Vanvitelli");
INSERT INTO teams (ip, name) VALUE ("10.60.13.1", "Universita' degli Studi dell'Aquila");
INSERT INTO teams (ip, name) VALUE ("10.60.14.1", "Universita' degli Studi dell'Insubria");
INSERT INTO teams (ip, name) VALUE ("10.60.15.1", "Universita' degli Studi di Bari Aldo Moro");
INSERT INTO teams (ip, name) VALUE ("10.60.16.1", "Universita' degli Studi di Brescia");
INSERT INTO teams (ip, name) VALUE ("10.60.17.1", "Universita' degli Studi di Cagliari");
INSERT INTO teams (ip, name) VALUE ("10.60.18.1", "Universita' degli Studi di Camerino");
INSERT INTO teams (ip, name) VALUE ("10.60.19.1", "Universita' degli studi di Cassino e del Lazio Meridionale");
INSERT INTO teams (ip, name) VALUE ("10.60.20.1", "Universita' degli Studi di Catania");
INSERT INTO teams (ip, name) VALUE ("10.60.21.1", "Universita' degli Studi di Ferrara");
INSERT INTO teams (ip, name) VALUE ("10.60.22.1", "Universita' degli Studi di Genova");
INSERT INTO teams (ip, name) VALUE ("10.60.23.1", "Universita' degli Studi di Messina");
INSERT INTO teams (ip, name) VALUE ("10.60.24.1", "Universita' degli Studi di Milano");
INSERT INTO teams (ip, name) VALUE ("10.60.25.1", "Universita' degli Studi di Milano-Bicocca");
INSERT INTO teams (ip, name) VALUE ("10.60.26.1", "Universita' degli Studi di Padova");
INSERT INTO teams (ip, name) VALUE ("10.60.27.1", "Universita' degli Studi di Palermo");
INSERT INTO teams (ip, name) VALUE ("10.60.28.1", "Universita' degli Studi di Parma");
INSERT INTO teams (ip, name) VALUE ("10.60.29.1", "Universita' degli Studi di Perugia");
INSERT INTO teams (ip, name) VALUE ("10.60.30.1", "Universita' degli Studi di Salerno");
INSERT INTO teams (ip, name) VALUE ("10.60.31.1", "Universita' degli Studi di Trento");
INSERT INTO teams (ip, name) VALUE ("10.60.32.1", "Universita' degli Studi di Udine");
INSERT INTO teams (ip, name) VALUE ("10.60.33.1", "Universita' degli Studi di Verona");
INSERT INTO teams (ip, name) VALUE ("10.60.34.1", "Universita' degli Studi 'Gabriele d'Annunzio'");
INSERT INTO teams (ip, name) VALUE ("10.60.35.1", "Universita' degli Studi Roma Tre");
INSERT INTO teams (ip, name) VALUE ("10.60.36.1", "Universita' della Calabria");
INSERT INTO teams (ip, name) VALUE ("10.60.37.1", "Universita' del Salento");
INSERT INTO teams (ip, name) VALUE ("10.60.38.1", "Universita' di Modena e Reggio Emilia");
INSERT INTO teams (ip, name) VALUE ("10.60.39.1", "Universita' di Napoli");
INSERT INTO teams (ip, name) VALUE ("10.60.40.1", "Universita' di Pisa");
INSERT INTO teams (ip, name) VALUE ("10.60.41.1", "Universita' di Torino");
INSERT INTO teams (ip, name) VALUE ("10.60.42.1", "Universita' Mediterranea di Reggio Calabria");
INSERT INTO teams (ip, name) VALUE ("10.60.43.1", "Universita' Politecnica delle March");

INSERT INTO `exploits` VALUES (1,'testExploit',16,60,10,'IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoKaW1wb3J0IHJhbmRvbQppbXBvcnQgc3RyaW5nCgpmb3IgXyBpbiByYW5nZSgxMCk6CiAgICBwcmludCgiIi5qb2luKHJhbmRvbS5jaG9pY2Uoc3RyaW5nLmFzY2lpX3VwcGVyY2FzZSkgZm9yIF8gaW4gcmFuZ2UoMzEpKSArICI9IiwgZmx1c2g9VHJ1ZSk=');
