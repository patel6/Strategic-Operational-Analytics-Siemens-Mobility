Metroville Urban Rail Expansion

KPI Development Framework (Strategic Operational Analytics)

This KPI framework aligns with Siemens Mobility’s project objectives across technical feasibility, sustainability, and community impact while integrating financial integrity and operational performance analytics.

1️⃣ Technical Feasibility KPIs
KPI 1

KPI Name: Track Installation Rate

Definition (What it measures):
Measures the speed of rail track installation per reporting period.

Measurement Method:
SUM(track_installed_meters) / reporting_period_days
Data Source: work_logs.csv

Rationale:
A leading indicator of construction momentum. Early slowdown signals downstream milestone delays.

KPI 2

KPI Name: On-Time Milestone Completion Rate

Definition:
Percentage of milestones completed on or before planned finish date.

Measurement Method:
COUNT(CASE WHEN actual_finish <= planned_finish THEN 1 END)
/ COUNT(completed_milestones)

Data Source: milestones.csv

Rationale:
Lagging performance metric indicating schedule adherence and execution effectiveness.

2️⃣ Environmental Sustainability KPIs
KPI 1

KPI Name: Downtime Efficiency Ratio

Definition:
Percentage of total working hours lost due to downtime events.

Measurement Method:
downtime_hours / hours_worked × 100

Data Source: work_logs.csv

Rationale:
Identifies operational inefficiencies that may increase emissions and resource waste.

KPI 2

KPI Name: Sustainability Incident Rate

Definition:
Number of safety incidents per 1,000 working hours.

Measurement Method:
(total_safety_incidents / total_hours_worked) × 1000

Data Source: work_logs.csv

Rationale:
Ensures compliance with environmental and safety regulations.

3️⃣ Community Acceptance KPIs
KPI 1

KPI Name: Delay Reason Distribution

Definition:
Distribution of delays categorized by permits, utilities, supply chain, regulatory or community-related causes.

Measurement Method:
Percentage breakdown of delay_reason field in milestones.csv

Rationale:
High regulatory/community delay share indicates stakeholder alignment challenges.

KPI 2

KPI Name: Issue Resolution Cycle Time

Definition:
Average number of days from issue_opened to issue_closed.

Measurement Method:
AVG(date_closed − date_opened)

Data Source: issues_risks.csv

Rationale:
Measures responsiveness to stakeholder concerns and operational disruptions.

4️⃣ Financial Integrity & Revenue Protection (Advanced Analytics Layer)

(Extension beyond basic template to support financial oversight)

KPI 1

KPI Name: Invoice Mismatch Rate

Definition:
Percentage of invoices where billed rate exceeds contract rate OR billed quantity exceeds approved quantity.

Measurement Method:
Computed using SQL CTE-based audit logic.

Data Source: invoices.csv + vendors.csv

Rationale:
Leading indicator of potential revenue leakage.

KPI 2

KPI Name: Duplicate Invoice Detection

Definition:
Invoices sharing same vendor_id + invoice_reference + billed_amount.

Measurement Method:
Window Function:
COUNT(*) OVER (PARTITION BY vendor_id, invoice_reference, billed_amount)

Rationale:
Prevents financial leakage and contract non-compliance.
