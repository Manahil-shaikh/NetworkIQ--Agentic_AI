from dataclasses import dataclass


@dataclass(frozen=True)
class AnomalyThresholds:
    """Thresholds used for basic telecom KPI anomaly detection."""

    max_prb_utilization: float = 90.0
    min_rsrp_dbm: float = -105.0
    min_sinr_db: float = 5.0
    max_call_drop_rate_pct: float = 2.0
    min_handover_success_rate_pct: float = 95.0
    min_rrc_setup_success_rate_pct: float = 97.0


@dataclass(frozen=True)
class Anomaly:
    """Represents a detected network anomaly."""

    kpi: str
    value: float
    threshold: float
    severity: str
    description: str


def detect_anomalies(
    row,
    thresholds: AnomalyThresholds | None = None,
) -> list[Anomaly]:
    """
    Detect KPI anomalies for a single cell observation.
    """

    if thresholds is None:
        thresholds = AnomalyThresholds()

    anomalies: list[Anomaly] = []

    # --------------------------------------------------
    # PRB utilization
    # --------------------------------------------------

    if row["prb_utilization_pct"] > thresholds.max_prb_utilization:
        anomalies.append(
            Anomaly(
                kpi="prb_utilization_pct",
                value=float(row["prb_utilization_pct"]),
                threshold=thresholds.max_prb_utilization,
                severity="HIGH",
                description=(
                    "PRB utilization is above the congestion threshold."
                ),
            )
        )

    # --------------------------------------------------
    # RSRP
    # --------------------------------------------------

    if row["rsrp_dbm"] < thresholds.min_rsrp_dbm:
        anomalies.append(
            Anomaly(
                kpi="rsrp_dbm",
                value=float(row["rsrp_dbm"]),
                threshold=thresholds.min_rsrp_dbm,
                severity="HIGH",
                description=(
                    "RSRP is below the minimum acceptable level."
                ),
            )
        )

    # --------------------------------------------------
    # SINR
    # --------------------------------------------------

    if row["sinr_db"] < thresholds.min_sinr_db:
        anomalies.append(
            Anomaly(
                kpi="sinr_db",
                value=float(row["sinr_db"]),
                threshold=thresholds.min_sinr_db,
                severity="HIGH",
                description=(
                    "SINR is below the minimum acceptable level."
                ),
            )
        )

    # --------------------------------------------------
    # Call drop rate
    # --------------------------------------------------

    if row["call_drop_rate_pct"] > thresholds.max_call_drop_rate_pct:
        anomalies.append(
            Anomaly(
                kpi="call_drop_rate_pct",
                value=float(row["call_drop_rate_pct"]),
                threshold=thresholds.max_call_drop_rate_pct,
                severity="HIGH",
                description=(
                    "Call drop rate is above the acceptable threshold."
                ),
            )
        )

    # --------------------------------------------------
    # Handover success
    # --------------------------------------------------

    if (
        row["handover_success_rate_pct"]
        < thresholds.min_handover_success_rate_pct
    ):
        anomalies.append(
            Anomaly(
                kpi="handover_success_rate_pct",
                value=float(row["handover_success_rate_pct"]),
                threshold=thresholds.min_handover_success_rate_pct,
                severity="MEDIUM",
                description=(
                    "Handover success rate is below the target."
                ),
            )
        )

    # --------------------------------------------------
    # RRC setup success
    # --------------------------------------------------

    if (
        row["rrc_setup_success_rate_pct"]
        < thresholds.min_rrc_setup_success_rate_pct
    ):
        anomalies.append(
            Anomaly(
                kpi="rrc_setup_success_rate_pct",
                value=float(row["rrc_setup_success_rate_pct"]),
                threshold=thresholds.min_rrc_setup_success_rate_pct,
                severity="MEDIUM",
                description=(
                    "RRC setup success rate is below the target."
                ),
            )
        )

    return anomalies