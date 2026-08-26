from pathlib import Path

from networkiq.data.repositories import NetworkRepository
from networkiq.detection.anomaly import detect_anomalies


def main() -> None:
    repository = NetworkRepository(Path("C:/personal/Projects/Telecom_Agentic_AI_2/data"))

    kpis = repository.get_kpis(
        cell_id="ISB_002"
    )

    for _, row in kpis.iterrows():

        anomalies = detect_anomalies(row)

        print(f"\nDate: {row['timestamp']}")
        print(f"Cell: {row['cell_id']}")

        if not anomalies:
            print("No anomalies detected.")
            continue

        print("Anomalies:")

        for anomaly in anomalies:
            print(
                f"  [{anomaly.severity}] "
                f"{anomaly.kpi}: "
                f"{anomaly.value} "
                f"(threshold: {anomaly.threshold})"
            )


if __name__ == "__main__":
    main()