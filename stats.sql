-- Flag stats all time
SELECT 
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected
FROM flags;

-- flags per tick last 15
SELECT 
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected,
    (end_time - MOD(end_time, 120)) AS tick_start
FROM runs INNER JOIN flags ON runs.id = flags.run_id
GROUP BY tick_start
ORDER BY tick_start DESC
LIMIT 15;


-- flags per script per team
SELECT 
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected
FROM flags INNER JOIN runs ON runs.id = flags.run_id
WHERE runs.exploit_id = ? AND runs.team_id = ?;


-- flags per script per team last tick
SELECT 
    runs.team_id AS team,
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected,
    (end_time - MOD(end_time, 120)) AS tick_start
FROM flags INNER JOIN runs ON runs.id = flags.run_id
WHERE runs.exploit_id = 1
GROUP BY tick_start, runs.team_id
ORDER BY tick_start DESC
LIMIT 1;


-- flags per script per tick
SELECT 
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected,
    (end_time - MOD(end_time, 120)) AS tick_start
FROM runs INNER JOIN flags ON runs.id = flags.run_id
WHERE runs.exploit_id = ?
GROUP BY tick_start;