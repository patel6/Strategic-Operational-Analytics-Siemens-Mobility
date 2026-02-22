## Project Overview

This project simulates an end-to-end operational analytics solution for a Siemens Mobility urban rail expansion program. 

It integrates schedule performance, operational efficiency, and financial audit logic to identify:

- Revenue leakage at the vendor level  
- Segment-level productivity bottlenecks  
- Schedule adherence risks  

The solution combines advanced SQL (CTEs, window functions), Python-based data generation, and Tableau dashboards to support executive decision-making.

Key Findings


1️⃣ Schedule Performance

75% of milestones were completed on time.

Remaining delays were concentrated in high-downtime segments.

2️⃣ Operational Bottlenecks

Segment 6 and Segment 2 show the highest downtime ratios (~15%+).

These segments likely contribute to downstream schedule risks.

3️⃣ Revenue Leakage

Vendor 2 accounts for the largest overbilling exposure (~$30K+).

Invoice mismatch rate stands at ~64%, indicating financial control gaps.

Duplicate and rate mismatch patterns suggest need for tighter AP validation.

4️⃣ Efficiency Indicators

Average track installation rate: ~2,165 meters/week.

Downtime ratio overall: ~8%.

## Executive Dashboard Preview

![Executive Overview](assets/executive_overview.png)
