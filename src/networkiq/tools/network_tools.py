from pathlib import Path

from langchain_core.tools import tool

from networkiq.data.repositories import NetworkRepository


repository = NetworkRepository(
    Path("C:/personal/Projects/Telecom_Agentic_AI_2/data")
)


@tool
def get_network_kpis(
    cell_id: str,
    region: str | None = None,
) -> list[dict]:
    """
    Retrieve network KPI measurements for a specific cell.

    Use this tool when you need network performance metrics
    such as PRB utilization, RSRP, SINR, throughput,
    call drop rate, handover success rate, or active users.

    Args:
        cell_id: Unique network cell identifier, e.g. ISB_002.
        region: Optional region filter, e.g. Islamabad.

    Returns:
        List of KPI records for the requested cell.
    """

    df = repository.get_kpis(
        cell_id=cell_id,
        region=region,
    )

    return df.to_dict(orient="records")


@tool
def get_cell_info(
    cell_id: str,
) -> list[dict]:
    """
    Retrieve metadata for a specific network cell.

    Use this when you need information such as region,
    technology, vendor, frequency band, or site.

    Args:
        cell_id: Unique network cell identifier.

    Returns:
        Cell metadata.
    """

    df = repository.get_cell(cell_id)

    return df.to_dict(orient="records")


@tool
def get_recent_incidents(
    cell_id: str,
) -> list[dict]:
    """
    Retrieve historical network incidents for a cell.

    Use this when investigating whether a cell has experienced
    previous problems such as congestion, interference,
    coverage degradation, or hardware issues.

    Args:
        cell_id: Unique network cell identifier.

    Returns:
        Historical incidents associated with the cell.
    """

    df = repository.get_incidents(
        cell_id=cell_id,
    )

    return df.to_dict(orient="records")