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

SELECT
    exploits.name,
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected
FROM (runs INNER JOIN flags ON runs.id = flags.run_id) INNER JOIN exploits ON runs.exploit_id = exploits.id
GROUP BY runs.exploit_id, exploits.name;

SELECT 
    team_id,
    COUNT(*)
FROM 


SELECT 
    (end_time - MOD(end_time, 120)) AS tick_start 
FROM runs 
GROUP BY tick_start 
ORDER BY tick_start DESC 
LIMIT 1, 1;

SELECT 
    exploits.id,
    tab1.flags,
    tab1.tick_start
FROM exploits LEFT JOIN (
    SELECT 
        runs.exploit_id AS expl_id,
        COUNT(*) AS flags,
        (runs.end_time - MOD(runs.end_time, 120)) AS tick_start 
    FROM flags INNER JOIN runs ON run_id = runs.id
    GROUP BY tick_start, runs.exploit_id
) AS tab1 ON exploits.id = tab1.expl_id
WHERE tab1.tick_start = 1687269000

SELECT *
FROM
(SELECT 
        (end_time - MOD(end_time, 120)) AS tick_start 
    FROM runs 
    GROUP BY tick_start 
    ORDER BY tick_start DESC 
    LIMIT 1, 1
) AS tab2 INNER JOIN (

) as tab3 ON tab2.tick_start = tab3.tick_start


CASE tab1.flags WHEN NULL THEN 0 else tab1.flags,


SELECT 
    exploits.id,
    COALESCE(tab1.flags, 0) as flags
FROM exploits LEFT JOIN (
    SELECT 
        runs.exploit_id AS expl_id,
        COUNT(*) AS flags,
        (runs.end_time - MOD(runs.end_time, 120)) AS tick_start 
    FROM flags INNER JOIN runs ON run_id = runs.id
    GROUP BY tick_start, runs.exploit_id
    HAVING tick_start = 1687270320
) AS tab1 ON exploits.id = tab1.expl_id;


SELECT 
    runs.team_id,
    COUNT(*) AS total,
    SUM(status=0) AS queued,
    SUM(status=1) AS accepted,
    SUM(status=2) AS rejected,
    (end_time - MOD(end_time, 120)) AS tick_start
FROM runs INNER JOIN flags ON runs.id = flags.run_id
WHERE runs.exploit_id = 1
GROUP BY tick_start, runs.team_id
HAVING tick_start = (
    SELECT
    (end_time - MOD(end_time, 120)) AS tick_start 
    FROM runs 
    GROUP BY tick_start 
    ORDER BY tick_start DESC 
    LIMIT 1, 1
)