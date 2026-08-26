from typing import Any, TypedDict

from langgraph.graph.message import add_messages
from typing_extensions import Annotated


class NetworkState(TypedDict, total=False):
    """
    Shared state for the NetworkIQ LangGraph workflow.
    """

    request: str

    cell_id: str | None
    region: str | None

    kpis: list[dict[str, Any]]
    anomalies: list[dict[str, Any]]
    incidents: list[dict[str, Any]]

    root_cause: str | None
    recommendation: str | None

    final_response: str | None

    messages: Annotated[list, add_messages]