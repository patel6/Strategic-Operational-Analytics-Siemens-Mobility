/* Bottleneck Analysis – Segment Level Performance */

WITH productivity AS (
    SELECT
        segment_id,
        SUM(track_installed_meters) AS total_meters,
        SUM(hours_worked) AS total_hours,
        SUM(downtime_hours) AS total_downtime,
        SUM(rework_hours) AS total_rework
    FROM work_logs
    GROUP BY segment_id
),

kpis AS (
    SELECT
        segment_id,
        total_meters,
        total_hours,
        total_downtime,
        total_rework,
        (total_meters / NULLIF(total_hours,0)) AS meters_per_hour,
        (total_downtime / NULLIF(total_hours,0)) * 100 AS downtime_pct,
        (total_rework / NULLIF(total_hours,0)) * 100 AS rework_pct
    FROM productivity
)

SELECT *
FROM kpis
ORDER BY downtime_pct DESC, rework_pct DESC;
