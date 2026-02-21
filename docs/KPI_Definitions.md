KPI Strategy – Urban Rail Expansion Program

Strategic Operational Analytics Simulation

This KPI framework aligns project execution with Siemens Mobility’s objectives in delivery performance, sustainability, financial integrity, and stakeholder accountability.

1. Strategic Objectives

The rail expansion program aims to:

Deliver infrastructure on schedule

Control project costs and prevent revenue leakage

Improve operational efficiency

Ensure environmental sustainability

Maintain regulatory and safety compliance

2. KPI Classification Framework

KPIs are categorized as:

Leading KPIs – Predict future performance
Lagging KPIs – Measure historical outcomes

3. Schedule & Construction KPIs
1. Track Installation Rate (Leading)

Measures construction velocity.

Formula:
SUM(track_installed_meters) / reporting_period_days

Target: ≥ planned installation baseline

Stakeholders: Engineering, Project Management

2. On-Time Milestone Rate (Lagging)

Measures schedule adherence.

Formula:
Completed_On_Time / Total_Completed_Milestones × 100

Target: ≥ 90%

Stakeholders: Program Director, City Authority

3. Critical Path Delay Impact (Lagging)

Total delay days for critical path milestones.

Formula:
SUM(actual_finish − planned_finish)
WHERE critical_path_flag = 'Y'

4. Financial Integrity & Revenue Leakage KPIs
4. Invoice Mismatch Rate (Leading)

Detects billing irregularities early.

Condition:

billed_qty ≠ approved_qty
OR

billed_rate > contract_rate

Formula:
Flagged_Invoices / Total_Invoices × 100

Target: < 5%

Stakeholders: Finance Controller

5. Duplicate Invoice Detection (Leading)

Identifies duplicate billing patterns using window functions.

Condition:
Same vendor_id + invoice_reference + billed_amount appears more than once.

6. Cost Variance (%) (Lagging)

Formula:
(Actual_Cost − Budgeted_Cost) / Budgeted_Cost

Target: Within ±3%

7. Overbilling Amount ($) (Lagging)

Formula:
SUM(billed_amount − approved_amount)
WHERE billed_amount > approved_amount

5. Productivity & Operational Efficiency KPIs
8. Crew Utilization Proxy (Leading)

Formula:
track_installed_meters / (crew_count × hours_worked)

Used to detect underperforming segments.

9. Downtime Ratio (%) (Leading)

Formula:
downtime_hours / total_hours_worked × 100

Target: < 10%

10. Rework Rate (%) (Lagging)

Formula:
rework_hours / total_hours_worked × 100

High rework correlates with quality issues.

6. Sustainability & Compliance KPIs
11. Incident Rate (Lagging)

Formula:
(total_incidents / total_hours_worked) × 1000

12. Delay Reason Distribution (Diagnostic KPI)

Tracks distribution across:

Permits

Supply chain

Weather

Labor

Community / regulatory

Used for root cause prioritization.
