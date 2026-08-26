from pathlib import Path
from networkiq.config import DATA_DIR
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from networkiq.data.repositories import NetworkRepository
from networkiq.detection.anomaly import (
    detect_anomalies as detect_kpi_anomalies,
)
from networkiq.llm.ollama import create_llm
from networkiq.llm.prompts import RCA_PROMPT
from networkiq.models.state import NetworkState
from networkiq.tools.network_tools import (
    get_cell_info,
    get_network_kpis,
    get_recent_incidents,
)


# ============================================================
# Dependencies
# ============================================================

# repository = NetworkRepository(
#     Path("C:/personal/Projects/Telecom_Agentic_AI_2/data")
# )
repository = NetworkRepository(DATA_DIR)

llm = create_llm()


# ============================================================
# Tools
# ============================================================

tools = [
    get_network_kpis,
    get_cell_info,
    get_recent_incidents,
]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)


# ============================================================
# Agent Node
# ============================================================

def call_model(state: NetworkState) -> NetworkState:
    """
    Invoke the LLM with the current conversation state.

    The LLM can either:
    - request a tool
    - provide a final investigation response
    """

    print("\n[Node] call_model")

    messages = state.get("messages", [])

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response],
    }


# ============================================================
# Agent Router
# ============================================================

def route_after_agent(state: NetworkState):
    """
    Decide whether the agent should execute tools or
    move into deterministic NetworkIQ analysis.
    """

    print("[Router] route_after_agent")

    messages = state.get("messages", [])

    if not messages:
        return "analyze_network"

    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        print("[Router] Tool call detected")
        return "tools"

    print("[Router] Investigation complete")
    return "analyze_network"


# ============================================================
# Network Analysis
# ============================================================

def analyze_network(state: NetworkState) -> NetworkState:
    """
    Retrieve network data and run deterministic anomaly detection.

    This is intentionally performed by Python rather than the LLM.
    """

    print("\n[Node] analyze_network")

    cell_id = state.get("cell_id")
    region = state.get("region")

    if not cell_id:
        return {
            "kpis": [],
            "incidents": [],
            "anomalies": [],
        }

    # --------------------------------------------------------
    # Retrieve KPI data
    # --------------------------------------------------------
    kpis_df = repository.get_kpis(
        cell_id=cell_id,
        region=region,
    )

    incidents_df = repository.get_incidents(
        cell_id=cell_id,
    )

    kpi_records = kpis_df.to_dict(
        orient="records"
    )

    incident_records = incidents_df.to_dict(
        orient="records"
    )

    all_anomalies = []

    for row in kpi_records:

        anomalies = detect_kpi_anomalies(row)

        all_anomalies.extend(
            {
                "timestamp": row.get("timestamp"),
                "kpi": anomaly.kpi,
                "value": anomaly.value,
                "threshold": anomaly.threshold,
                "severity": anomaly.severity,
                "description": anomaly.description,
            }
            for anomaly in anomalies
        )

    return {
        "kpis": kpi_records,
        "incidents": incident_records,
        "anomalies": all_anomalies,
    }


# ============================================================
# Root Cause Analysis
# ============================================================

def analyze_root_cause(state: NetworkState) -> NetworkState:
    """
    Ask the LLM to interpret deterministic network evidence.
    """

    print("\n[Node] analyze_root_cause")

    evidence = {
        "cell_id": state.get("cell_id"),
        "region": state.get("region"),
        "kpis": state.get("kpis", []),
        "anomalies": state.get("anomalies", []),
        "historical_incidents": state.get(
            "incidents",
            [],
        ),
    }

    prompt = RCA_PROMPT.format(
        evidence=evidence
    )

    response = llm.invoke(prompt)

    return {
        "root_cause": response.content,
    }


# ============================================================
# Recommendation
# ============================================================

def generate_recommendation(
    state: NetworkState,
) -> NetworkState:
    """
    Generate a simple recommendation based on the
    detected anomalies and RCA.
    """

    print("\n[Node] generate_recommendation")

    anomalies = state.get("anomalies", [])
    root_cause = state.get("root_cause", "")

    recommendation_prompt = f"""
You are NetworkIQ, a telecom network optimization assistant.

Based ONLY on the evidence below, provide practical
network-engineering recommendations.

Root cause analysis:
{root_cause}

Detected anomalies:
{anomalies}

Provide:
1. Immediate action
2. Follow-up investigation
3. What KPI should be monitored

Do not invent measurements or configuration values.
Keep the response concise.
"""

    response = llm.invoke(
        recommendation_prompt
    )

    return {
        "recommendation": response.content,
    }


# ============================================================
# Final Response
# ============================================================

def build_final_response(
    state: NetworkState,
) -> NetworkState:
    """
    Combine the investigation, RCA, and recommendation
    into the final NetworkIQ response.
    """

    print("\n[Node] build_final_response")

    cell_id = state.get("cell_id")

    root_cause = state.get(
        "root_cause",
        "No root-cause analysis available.",
    )

    recommendation = state.get(
        "recommendation",
        "No recommendation available.",
    )

    anomalies = state.get(
        "anomalies",
        [],
    )

    if anomalies:
        anomaly_summary = "\n".join(
            f"- [{item['severity']}] "
            f"{item['kpi']}: "
            f"{item['value']} "
            f"(threshold {item['threshold']})"
            for item in anomalies
        )
    else:
        anomaly_summary = "No anomalies detected."

    final_response = f"""
NetworkIQ Investigation
=======================

Cell:
{cell_id}

Detected Anomalies:
{anomaly_summary}

Root Cause Analysis:
{root_cause}

Recommendations:
{recommendation}
""".strip()

    return {
        "final_response": final_response,
    }


# ============================================================
# Build Graph
# ============================================================

def build_agent_graph():
    """
    Build the complete NetworkIQ agent graph.
    """

    graph = StateGraph(NetworkState)

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    graph.add_node(
        "call_model",
        call_model,
    )

    graph.add_node(
        "tools",
        tool_node,
    )

    graph.add_node(
        "analyze_network",
        analyze_network,
    )

    graph.add_node(
        "analyze_root_cause",
        analyze_root_cause,
    )

    graph.add_node(
        "generate_recommendation",
        generate_recommendation,
    )

    graph.add_node(
        "build_final_response",
        build_final_response,
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    graph.add_edge(
        START,
        "call_model",
    )

    # --------------------------------------------------------
    # Agent routing
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "call_model",
        route_after_agent,
        {
            "tools": "tools",
            "analyze_network": "analyze_network",
        },
    )

    # --------------------------------------------------------
    # Tool -> Agent
    # --------------------------------------------------------

    graph.add_edge(
        "tools",
        "call_model",
    )

    # --------------------------------------------------------
    # Network analysis pipeline
    # --------------------------------------------------------

    graph.add_edge(
        "analyze_network",
        "analyze_root_cause",
    )

    graph.add_edge(
        "analyze_root_cause",
        "generate_recommendation",
    )

    graph.add_edge(
        "generate_recommendation",
        "build_final_response",
    )

    # --------------------------------------------------------
    # END
    # --------------------------------------------------------

    graph.add_edge(
        "build_final_response",
        END,
    )

    return graph.compile()