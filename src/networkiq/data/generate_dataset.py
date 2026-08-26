from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd


random.seed(42)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Cell metadata
# ---------------------------------------------------------

cells = [
    {
        "cell_id": "ISB_001",
        "site_id": "SITE_ISB_001",
        "region": "Islamabad",
        "technology": "4G",
        "vendor": "Ericsson",
        "band": "B3",
        "latitude": 33.6844,
        "longitude": 73.0479,
    },
    {
        "cell_id": "ISB_002",
        "site_id": "SITE_ISB_001",
        "region": "Islamabad",
        "technology": "4G",
        "vendor": "Ericsson",
        "band": "B3",
        "latitude": 33.6844,
        "longitude": 73.0479,
    },
    {
        "cell_id": "ISB_003",
        "site_id": "SITE_ISB_002",
        "region": "Islamabad",
        "technology": "5G",
        "vendor": "Nokia",
        "band": "n78",
        "latitude": 33.7000,
        "longitude": 73.0600,
    },
    {
        "cell_id": "RWP_001",
        "site_id": "SITE_RWP_001",
        "region": "Rawalpindi",
        "technology": "5G",
        "vendor": "Nokia",
        "band": "n78",
        "latitude": 33.5651,
        "longitude": 73.0169,
    },
    {
        "cell_id": "RWP_002",
        "site_id": "SITE_RWP_002",
        "region": "Rawalpindi",
        "technology": "4G",
        "vendor": "Huawei",
        "band": "B1",
        "latitude": 33.5900,
        "longitude": 73.0500,
    },
    {
        "cell_id": "LHR_001",
        "site_id": "SITE_LHR_001",
        "region": "Lahore",
        "technology": "4G",
        "vendor": "Huawei",
        "band": "B3",
        "latitude": 31.5204,
        "longitude": 74.3587,
    },
    {
        "cell_id": "LHR_002",
        "site_id": "SITE_LHR_002",
        "region": "Lahore",
        "technology": "5G",
        "vendor": "Ericsson",
        "band": "n78",
        "latitude": 31.5500,
        "longitude": 74.3400,
    },
]


cells_df = pd.DataFrame(cells)
cells_df.to_csv(DATA_DIR / "cells.csv", index=False)


# ---------------------------------------------------------
# KPI generation
# ---------------------------------------------------------

start_date = datetime(2026, 8, 20)

kpi_rows = []

for day in range(5):

    timestamp = start_date + timedelta(days=day)

    for cell in cells:

        cell_id = cell["cell_id"]

        # Normal baseline
        rsrp = random.uniform(-95, -80)
        sinr = random.uniform(10, 20)
        dl_throughput = random.uniform(35, 80)
        ul_throughput = random.uniform(8, 20)
        prb = random.uniform(40, 75)
        drop_rate = random.uniform(0.2, 1.2)
        ho_success = random.uniform(96, 99.5)
        rrc_success = random.uniform(97, 99.8)
        active_users = random.randint(80, 250)

        # -------------------------------------------------
        # Inject congestion anomaly
        # -------------------------------------------------

        if cell_id == "ISB_002":

            prb = random.uniform(92, 98)
            active_users = random.randint(350, 500)

            dl_throughput = random.uniform(10, 20)
            ul_throughput = random.uniform(3, 7)

            drop_rate = random.uniform(2.5, 5.0)

            ho_success = random.uniform(91, 95)

        # -------------------------------------------------
        # Inject interference anomaly
        # -------------------------------------------------

        elif cell_id == "RWP_001":

            sinr = random.uniform(1, 5)

            dl_throughput = random.uniform(12, 25)
            ul_throughput = random.uniform(3, 8)

            drop_rate = random.uniform(1.5, 3.0)

        # -------------------------------------------------
        # Inject coverage anomaly
        # -------------------------------------------------

        elif cell_id == "RWP_002":

            rsrp = random.uniform(-115, -103)

            sinr = random.uniform(4, 9)

            dl_throughput = random.uniform(15, 30)

            drop_rate = random.uniform(1.5, 3.5)

            ho_success = random.uniform(92, 96)

        kpi_rows.append(
            {
                "timestamp": timestamp.strftime("%Y-%m-%d"),
                "cell_id": cell_id,
                "region": cell["region"],
                "technology": cell["technology"],
                "rsrp_dbm": round(rsrp, 2),
                "sinr_db": round(sinr, 2),
                "dl_throughput_mbps": round(dl_throughput, 2),
                "ul_throughput_mbps": round(ul_throughput, 2),
                "prb_utilization_pct": round(prb, 2),
                "call_drop_rate_pct": round(drop_rate, 2),
                "handover_success_rate_pct": round(ho_success, 2),
                "rrc_setup_success_rate_pct": round(rrc_success, 2),
                "active_users": active_users,
            }
        )


kpis_df = pd.DataFrame(kpi_rows)

kpis_df.to_csv(
    DATA_DIR / "network_kpis.csv",
    index=False,
)


# ---------------------------------------------------------
# Incident history
# ---------------------------------------------------------

incidents = [
    {
        "incident_id": "INC_001",
        "timestamp": "2026-08-21",
        "cell_id": "ISB_002",
        "incident_type": "CONGESTION",
        "severity": "HIGH",
        "description": "High traffic load and elevated PRB utilization.",
    },
    {
        "incident_id": "INC_002",
        "timestamp": "2026-08-22",
        "cell_id": "RWP_001",
        "incident_type": "INTERFERENCE",
        "severity": "MEDIUM",
        "description": "Low SINR observed during peak hours.",
    },
    {
        "incident_id": "INC_003",
        "timestamp": "2026-08-23",
        "cell_id": "RWP_002",
        "incident_type": "COVERAGE",
        "severity": "HIGH",
        "description": "Poor RSRP and degraded mobility performance.",
    },
]

incidents_df = pd.DataFrame(incidents)

incidents_df.to_csv(
    DATA_DIR / "incidents.csv",
    index=False,
)


print("Dataset generated successfully.")
print(f"Data directory: {DATA_DIR}")
print(f"Cells: {len(cells_df)}")
print(f"KPI rows: {len(kpis_df)}")
print(f"Incidents: {len(incidents_df)}")