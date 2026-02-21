KPI Definitions – Strategic Operational Analytics

Urban Rail Expansion Simulation

This document defines the key performance indicators (KPIs) used to evaluate schedule performance, financial integrity, productivity, and safety across the rail expansion program.

1. Schedule & Delivery KPIs
On-Time Milestone Rate (%)

Definition:
Percentage of completed milestones delivered on or before planned finish date.

Formula:
Completed_On_Time / Total_Completed_Milestones * 100

Business Goal:
Maintain > 90% on-time completion rate.

Schedule Variance (%)

Definition:
Difference between planned progress and actual progress.

Formula:
(Planned_Progress_% − Actual_Progress_%)

Positive = Behind schedule
Negative = Ahead of schedule

Critical Path Delay Impact (Days)

Definition:
Total delay days for milestones flagged as critical path.

Formula:
SUM(Actual_Finish − Planned_Finish)
WHERE Critical_Path_Flag = 'Y'

2. Financial Integrity & Revenue Leakage KPIs
Cost Variance (%)

Definition:
Variance between actual spend and budgeted spend.

Formula:
(Actual_Cost − Budgeted_Cost) / Budgeted_Cost

Invoice Mismatch Rate (%)

Definition:
Percentage of invoices where billed values do not match approved values.

Conditions:

billed_qty ≠ approved_qty
OR

billed_rate > contract_rate

Formula:
Flagged_Invoices / Total_Invoices * 100

Duplicate Invoice Indicator

Definition:
Invoices with identical:

vendor_id

invoice_reference

billed_amount

Detected using SQL window functions.

Overbilling Amount ($)

Definition:
Total amount billed above approved values.

Formula:
SUM(billed_amount − approved_amount)
WHERE billed_amount > approved_amount

3. Productivity & Operational Efficiency KPIs
Track Installation Rate (meters/day)

Definition:
Average track installed per working day.

Formula:
SUM(track_installed_meters) / COUNT(DISTINCT work_date)

Crew Utilization Proxy

Definition:
Productivity per crew-hour.

Formula:
track_installed_meters / (crew_count * hours_worked)

Downtime Ratio (%)

Definition:
Percentage of total working hours lost due to downtime.

Formula:
downtime_hours / total_hours_worked * 100

Rework Rate (%)

Definition:
Percentage of hours spent on rework activities.

Formula:
rework_hours / total_hours_worked * 100

4. Safety & Sustainability KPIs
Incident Rate

Definition:
Number of safety incidents per 1,000 work hours.

Formula:
(total_incidents / total_hours_worked) * 1000

Delay Reason Distribution

Definition:
Percentage breakdown of delay causes:

Permits

Supply Chain

Weather

Labor

Community / Regulatory

Used for root cause bottleneck analysis.
