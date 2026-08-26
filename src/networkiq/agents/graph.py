from pathlib import Path

from langgraph.graph import END, START, StateGraph

from networkiq.data.repositories import NetworkRepository
from networkiq.detection.anomaly import (
    detect_anomalies as detect_kpi_anomalies,
)
from networkiq.llm.ollama import create_llm
from networkiq.llm.prompts import RCA_PROMPT
from networkiq.models.state import NetworkState


# ---------------------------------------------------------
# Dependencies
# ---------------------------------------------------------

repository = NetworkRepository(
    Path("C:/personal/Projects/Telecom_Agentic_AI_2/data")
)

llm = create_llm()


# ---------------------------------------------------------
# Nodes
# ---------------------------------------------------------

def understand_request(state: NetworkState) -> NetworkState:
    print("Node: understand_request")

    return state


def retrieve_data(state: NetworkState) -> NetworkState:
    print("Node: retrieve_data")

    cell_id = state.get("cell_id")
    region = state.get("region")

    if not cell_id:
        return {
            "kpis": [],
            "incidents": [],
        }

    kpis = repository.get_kpis(
        cell_id=cell_id,
        region=region,
    )

    incidents = repository.get_incidents(
        cell_id=cell_id,
    )

    return {
        "kpis": kpis.to_dict(orient="records"),
        "incidents": incidents.to_dict(orient="records"),
    }


def detect_anomalies(state: NetworkState) -> NetworkState:
    print("Node: detect_anomalies")

    kpis = state.get("kpis", [])

    all_anomalies = []

    for row in kpis:

        anomalies = detect_kpi_anomalies(row)

        all_anomalies.extend(
            {
                "kpi": anomaly.kpi,
                "value": anomaly.value,
                "threshold": anomaly.threshold,
                "severity": anomaly.severity,
                "description": anomaly.description,
            }
            for anomaly in anomalies
        )

    return {
        "anomalies": all_anomalies,
    }


def analyze_root_cause(state: NetworkState) -> NetworkState:
    print("Node: analyze_root_cause")

    kpis = state.get("kpis", [])
    anomalies = state.get("anomalies", [])
    incidents = state.get("incidents", [])

    evidence = {
        "cell_id": state.get("cell_id"),
        "region": state.get("region"),
        "kpis": kpis,
        "anomalies": anomalies,
        "historical_incidents": incidents,
    }

    prompt = RCA_PROMPT.format(
        evidence=evidence
    )

    response = llm.invoke(prompt)

    return {
        "root_cause": response.content,
    }


def generate_recommendation(state: NetworkState) -> NetworkState:
    print("Node: generate_recommendation")

    return state


# ---------------------------------------------------------
# Graph
# ---------------------------------------------------------

def build_graph():
    graph = StateGraph(NetworkState)

    # Nodes
    graph.add_node(
        "understand_request",
        understand_request,
    )

    graph.add_node(
        "retrieve_data",
        retrieve_data,
    )

    graph.add_node(
        "detect_anomalies",
        detect_anomalies,
    )

    graph.add_node(
        "analyze_root_cause",
        analyze_root_cause,
    )

    graph.add_node(
        "generate_recommendation",
        generate_recommendation,
    )

    # Edges
    graph.add_edge(
        START,
        "understand_request",
    )

    graph.add_edge(
        "understand_request",
        "retrieve_data",
    )

    graph.add_edge(
        "retrieve_data",
        "detect_anomalies",
    )

    graph.add_edge(
        "detect_anomalies",
        "analyze_root_cause",
    )

    graph.add_edge(
        "analyze_root_cause",
        "generate_recommendation",
    )

    graph.add_edge(
        "generate_recommendation",
        END,
    )

    return graph.compile()