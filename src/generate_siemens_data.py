import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# Config (you can tweak later)
# -----------------------------
SEED = 42
PROJECT_ID = "P001"
CITY = "Metro City"
CORRIDOR = "Urban Rail Expansion"
N_SEGMENTS = 8

START_DATE = "2025-08-01"
END_DATE = "2025-12-31"
FREQ = "W-MON"  # weekly logs, Monday weeks

N_VENDORS = 10
LEAKAGE_RATE = 0.05  # subtle: ~5% of invoice lines get flagged patterns

OUT_RAW_DIR = os.path.join("data", "raw")

np.random.seed(SEED)

def ensure_dirs():
    os.makedirs(OUT_RAW_DIR, exist_ok=True)

def daterange_weeks(start, end, freq="W-MON"):
    return pd.date_range(start=start, end=end, freq=freq)

def make_projects():
    return pd.DataFrame([{
        "project_id": PROJECT_ID,
        "city": CITY,
        "corridor_name": CORRIDOR,
        "start_date": START_DATE,
        "planned_end_date": "2026-06-30",
        "budget_total": 250_000_000,
        "sponsor": "City Public Transport Authority",
        "program_goal": "Capacity + Sustainability"
    }])

def make_segments():
    contractors = [f"C{i:02d}" for i in range(1, 6)]
    rows = []
    for i in range(1, N_SEGMENTS + 1):
        rows.append({
            "segment_id": f"S{i:03d}",
            "project_id": PROJECT_ID,
            "segment_name": f"Segment {i}",
            "length_km": round(np.random.uniform(1.5, 4.5), 2),
            "contractor_id": np.random.choice(contractors),
            "region_zone": np.random.choice(["North", "South", "East", "West"])
        })
    return pd.DataFrame(rows)

def make_milestones(segments):
    milestone_templates = [
        ("Track Bed Prep", 21),
        ("Track Installation", 35),
        ("Electrification", 28),
        ("Signaling", 28),
        ("Testing & Commissioning", 21),
    ]
    delay_reasons = ["Permits", "Supply Chain", "Weather", "Labor", "Community/Regulatory", "Utilities"]
    rows = []
    base_start = datetime.fromisoformat(START_DATE)

    mid = 1
    for _, seg in segments.iterrows():
        seg_start = base_start + timedelta(days=int(np.random.uniform(0, 14)))
        current = seg_start
        for name, dur in milestone_templates:
            planned_start = current
            planned_finish = current + timedelta(days=dur)

            # delays
            delay_days = int(np.random.choice([0, 0, 0, 3, 5, 7, 10], p=[0.45, 0.2, 0.1, 0.1, 0.07, 0.05, 0.03]))
            actual_start = planned_start + timedelta(days=int(np.random.choice([0, 0, 1, 2], p=[0.6, 0.25, 0.1, 0.05])))
            actual_finish = planned_finish + timedelta(days=delay_days)

            status = "Completed" if actual_finish < datetime.fromisoformat(END_DATE) else "In Progress"
            delay_reason = np.random.choice(delay_reasons) if delay_days > 0 else ""

            rows.append({
                "milestone_id": f"M{mid:04d}",
                "project_id": PROJECT_ID,
                "segment_id": seg["segment_id"],
                "milestone_name": name,
                "planned_start": planned_start.date().isoformat(),
                "planned_finish": planned_finish.date().isoformat(),
                "actual_start": actual_start.date().isoformat(),
                "actual_finish": actual_finish.date().isoformat(),
                "status": status,
                "delay_reason": delay_reason,
                "critical_path_flag": "Y" if name in ["Track Installation", "Signaling"] else "N"
            })
            mid += 1
            current = planned_finish + timedelta(days=3)
    return pd.DataFrame(rows)

def make_vendors():
    service_types = ["Civil", "Electrical", "Signaling", "Materials", "Staffing"]
    unit_types = {"Civil": "hour", "Electrical": "hour", "Signaling": "hour", "Materials": "meter", "Staffing": "hour"}
    rows = []
    for i in range(1, N_VENDORS + 1):
        st = np.random.choice(service_types)
        base_rate = {
            "Civil": np.random.uniform(90, 130),
            "Electrical": np.random.uniform(95, 140),
            "Signaling": np.random.uniform(110, 160),
            "Materials": np.random.uniform(450, 750),
            "Staffing": np.random.uniform(60, 95),
        }[st]
        rows.append({
            "vendor_id": f"V{i:03d}",
            "vendor_name": f"Vendor {i}",
            "service_type": st,
            "contract_rate_per_unit": round(base_rate, 2),
            "unit_type": unit_types[st],
            "contract_start": START_DATE,
            "contract_end": "2026-06-30"
        })
    return pd.DataFrame(rows)

def make_work_logs(segments):
    weeks = daterange_weeks(START_DATE, END_DATE, FREQ)
    downtime_reasons = ["Permits", "Supply Chain", "Weather", "Labor", "Safety", "Utilities", "None"]
    rows = []
    lid = 1

    # make 2 segments slightly worse to create bottlenecks
    bottleneck_segments = set(np.random.choice(segments["segment_id"], size=2, replace=False))

    for d in weeks:
        for _, seg in segments.iterrows():
            seg_id = seg["segment_id"]
            crew = int(np.random.uniform(10, 28))
            hours = crew * int(np.random.choice([32, 36, 40], p=[0.2, 0.3, 0.5]))

            base_downtime = np.random.uniform(0, 0.12)
            if seg_id in bottleneck_segments:
                base_downtime += np.random.uniform(0.05, 0.12)

            downtime_hours = round(hours * min(base_downtime, 0.35), 2)
            downtime_reason = np.random.choice(downtime_reasons, p=[0.12, 0.15, 0.12, 0.08, 0.05, 0.08, 0.40])
            if downtime_hours < 5:
                downtime_reason = "None"

            # production lower when downtime higher
            max_weekly_meters = np.random.uniform(220, 420)
            produced = max_weekly_meters * (1 - downtime_hours / max(hours, 1))
            produced *= np.random.uniform(0.85, 1.1)
            if seg_id in bottleneck_segments:
                produced *= np.random.uniform(0.75, 0.95)

            rework_hours = round(np.random.uniform(0, 0.08) * hours, 2)
            if seg_id in bottleneck_segments:
                rework_hours = round(rework_hours * np.random.uniform(1.1, 1.6), 2)

            incidents = int(np.random.choice([0, 0, 0, 1, 2], p=[0.6, 0.2, 0.08, 0.1, 0.02]))

            rows.append({
                "log_id": f"L{lid:06d}",
                "week_start": d.date().isoformat(),
                "project_id": PROJECT_ID,
                "segment_id": seg_id,
                "crew_count": crew,
                "hours_worked": hours,
                "downtime_hours": downtime_hours,
                "downtime_reason": downtime_reason,
                "track_installed_meters": round(max(produced, 0), 2),
                "rework_hours": rework_hours,
                "safety_incidents": incidents,
                "notes": ""
            })
            lid += 1
    return pd.DataFrame(rows)

def make_invoices(segments, vendors):
    weeks = daterange_weeks(START_DATE, END_DATE, FREQ)
    rows = []
    inv_id = 1
    line_id = 1

    # choose a couple vendors that will have higher leakage patterns
    risky_vendors = set(np.random.choice(vendors["vendor_id"], size=2, replace=False))

    for d in weeks:
        for _ in range(np.random.randint(6, 12)):  # invoices per week
            vendor = vendors.sample(1).iloc[0]
            seg = segments.sample(1).iloc[0]

            vendor_id = vendor["vendor_id"]
            service_type = vendor["service_type"]
            contract_rate = float(vendor["contract_rate_per_unit"])

            # qty depends on unit type
            if vendor["unit_type"] == "meter":
                billed_qty = round(np.random.uniform(80, 260), 2)
            else:
                billed_qty = round(np.random.uniform(40, 160), 2)

            billed_rate = round(contract_rate * np.random.uniform(0.98, 1.03), 2)

            approved_qty = billed_qty
            approved_rate = billed_rate

            # inject leakage (rate mismatch / qty mismatch / duplicates)
            leak = np.random.rand() < LEAKAGE_RATE or (vendor_id in risky_vendors and np.random.rand() < (LEAKAGE_RATE * 1.6))

            leak_type = None
            if leak:
                leak_type = np.random.choice(["RATE", "QTY", "DUPLICATE"], p=[0.45, 0.45, 0.10])

            invoice_reference = f"REF-{vendor_id}-{d.strftime('%Y%m%d')}-{np.random.randint(1000,9999)}"
            po_number = f"PO-{np.random.randint(10000,99999)}"

            if leak_type == "RATE":
                billed_rate = round(contract_rate * np.random.uniform(1.06, 1.18), 2)  # above contract
                approved_rate = round(contract_rate, 2)
            elif leak_type == "QTY":
                approved_qty = round(billed_qty * np.random.uniform(0.82, 0.95), 2)
            elif leak_type == "DUPLICATE":
                # We'll intentionally reuse invoice_reference sometimes later
                pass

            billed_amount = round(billed_qty * billed_rate, 2)
            approved_amount = round(approved_qty * approved_rate, 2)

            approval_status = "Approved"
            if billed_amount > approved_amount:
                approval_status = np.random.choice(["Partial", "Approved"], p=[0.75, 0.25])

            payment_status = np.random.choice(["Paid", "Pending"], p=[0.7, 0.3])

            entered_by = np.random.choice(["AP_Analyst_1", "AP_Analyst_2", "Vendor_Portal", "Finance_Admin"])

            rows.append({
                "invoice_id": f"INV{inv_id:05d}",
                "invoice_line_id": f"LINE{line_id:06d}",
                "vendor_id": vendor_id,
                "project_id": PROJECT_ID,
                "segment_id": seg["segment_id"],
                "invoice_date": d.date().isoformat(),
                "service_type": service_type,
                "billed_qty": billed_qty,
                "billed_rate": billed_rate,
                "billed_amount": billed_amount,
                "approved_qty": approved_qty,
                "approved_rate": approved_rate,
                "approved_amount": approved_amount,
                "approval_status": approval_status,
                "payment_status": payment_status,
                "po_number": po_number,
                "invoice_reference": invoice_reference,
                "entered_by": entered_by
            })
            inv_id += 1
            line_id += 1

    invoices = pd.DataFrame(rows)

    # Create a small number of duplicates by copying some rows and reusing reference
    dup_n = max(3, int(len(invoices) * 0.01))
    dup_rows = invoices.sample(dup_n, random_state=SEED).copy()
    dup_rows["invoice_id"] = [f"INV{inv_id+i:05d}" for i in range(dup_n)]
    inv_id += dup_n
    invoices = pd.concat([invoices, dup_rows], ignore_index=True)

    return invoices

def make_issues(segments):
    categories = ["Permits", "Community/Regulatory", "Supply Chain", "Safety", "Budget", "Utilities"]
    rows = []
    iid = 1
    for _ in range(45):
        seg = segments.sample(1).iloc[0]
        opened = datetime.fromisoformat(START_DATE) + timedelta(days=int(np.random.uniform(0, 120)))
        days_open = int(np.random.uniform(3, 35))
        closed = opened + timedelta(days=days_open)
        severity = np.random.choice(["Low", "Medium", "High"], p=[0.5, 0.35, 0.15])
        cat = np.random.choice(categories)
        impact_days = int(np.random.uniform(0, 14)) if severity != "Low" else int(np.random.uniform(0, 6))
        cost_impact = int(np.random.uniform(5_000, 90_000)) if severity == "High" else int(np.random.uniform(1_000, 35_000))

        rows.append({
            "issue_id": f"ISS{iid:04d}",
            "project_id": PROJECT_ID,
            "segment_id": seg["segment_id"],
            "issue_type": np.random.choice(["Risk", "Issue"], p=[0.45, 0.55]),
            "category": cat,
            "severity": severity,
            "date_opened": opened.date().isoformat(),
            "date_closed": closed.date().isoformat(),
            "owner_role": np.random.choice(["PM", "Engineering", "Finance", "Vendor"], p=[0.4, 0.35, 0.15, 0.10]),
            "description": f"{cat} constraint affecting delivery timeline.",
            "impact_days": impact_days,
            "cost_impact_est": cost_impact
        })
        iid += 1
    return pd.DataFrame(rows)

def main():
    ensure_dirs()

    projects = make_projects()
    segments = make_segments()
    milestones = make_milestones(segments)
    vendors = make_vendors()
    work_logs = make_work_logs(segments)
    invoices = make_invoices(segments, vendors)
    issues = make_issues(segments)

    projects.to_csv(os.path.join(OUT_RAW_DIR, "projects.csv"), index=False)
    segments.to_csv(os.path.join(OUT_RAW_DIR, "segments.csv"), index=False)
    milestones.to_csv(os.path.join(OUT_RAW_DIR, "milestones.csv"), index=False)
    work_logs.to_csv(os.path.join(OUT_RAW_DIR, "work_logs.csv"), index=False)
    vendors.to_csv(os.path.join(OUT_RAW_DIR, "vendors.csv"), index=False)
    invoices.to_csv(os.path.join(OUT_RAW_DIR, "invoices.csv"), index=False)
    issues.to_csv(os.path.join(OUT_RAW_DIR, "issues_risks.csv"), index=False)

    print("✅ Synthetic data generated in data/raw/")
    print("Files:", ["projects.csv","segments.csv","milestones.csv","work_logs.csv","vendors.csv","invoices.csv","issues_risks.csv"])

if __name__ == "__main__":
    main()
