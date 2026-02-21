/* Executive KPI Summary */

-- On-Time Milestone Rate
WITH milestone_calc AS (
    SELECT
        COUNT(*) AS total_completed,
        SUM(CASE WHEN actual_finish <= planned_finish THEN 1 ELSE 0 END) AS on_time
    FROM milestones
    WHERE status = 'Completed'
)

SELECT
    (on_time * 1.0 / total_completed) * 100 AS on_time_rate_pct
FROM milestone_calc;
