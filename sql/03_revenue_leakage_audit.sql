/* Revenue Leakage Audit – Siemens Mobility (Simulation)
   Techniques: CTEs + Window Functions
*/

WITH base AS (
    SELECT
        i.*,
        v.contract_rate_per_unit AS contract_rate,
        CASE WHEN i.billed_rate > v.contract_rate_per_unit THEN 1 ELSE 0 END AS rate_mismatch_flag,
        CASE WHEN i.billed_qty <> i.approved_qty THEN 1 ELSE 0 END AS qty_mismatch_flag,
        CASE
            WHEN i.billed_amount > i.approved_amount THEN (i.billed_amount - i.approved_amount)
            ELSE 0
        END AS overbilled_amount
    FROM invoices i
    LEFT JOIN vendors v
        ON i.vendor_id = v.vendor_id
),
dupes AS (
    SELECT
        *,
        COUNT(*) OVER (PARTITION BY vendor_id, invoice_reference, billed_amount) AS dup_count
    FROM base
),
flags AS (
    SELECT
        *,
        CASE WHEN dup_count > 1 THEN 1 ELSE 0 END AS duplicate_invoice_flag,
        CASE
            WHEN (rate_mismatch_flag = 1 OR qty_mismatch_flag = 1 OR dup_count > 1) THEN 1
            ELSE 0
        END AS leakage_flag,
        CASE
            WHEN dup_count > 1 THEN 'DUPLICATE'
            WHEN rate_mismatch_flag = 1 THEN 'RATE_MISMATCH'
            WHEN qty_mismatch_flag = 1 THEN 'QTY_MISMATCH'
            ELSE 'OK'
        END AS leakage_reason
    FROM dupes
)

SELECT
    vendor_id,
    leakage_reason,
    COUNT(*) AS invoice_lines,
    SUM(overbilled_amount) AS total_overbilled_amount
FROM flags
WHERE leakage_flag = 1
GROUP BY vendor_id, leakage_reason
ORDER BY total_overbilled_amount DESC;
