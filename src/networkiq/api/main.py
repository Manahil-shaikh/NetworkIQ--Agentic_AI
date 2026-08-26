from fastapi import FastAPI, HTTPException

from langchain_core.messages import HumanMessage

from networkiq.agents.agent_graph import build_agent_graph
from networkiq.agents.request_parser import parse_request
from networkiq.api.schemas import (
    InvestigationRequest,
    InvestigationResponse,
)
from networkiq.config import APP_NAME, ENVIRONMENT


app = FastAPI(
    title=APP_NAME,
    description="Agentic Telecom Network Intelligence System",
    version="0.1.0",
)


# Build the graph once when the API process starts.
graph = build_agent_graph()


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "ok",
        "application": APP_NAME,
        "environment": ENVIRONMENT,
    }


@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)
def investigate(
    request: InvestigationRequest,
):
    """
    Run a NetworkIQ investigation.
    """

    # --------------------------------------------------------
    # Parse user request
    # --------------------------------------------------------

    parsed = parse_request(
        request.query
    )

    cell_id = parsed.get("cell_id")
    region = parsed.get("region")

    if not cell_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not identify a cell ID. "
                "Please provide a cell such as ISB_002."
            ),
        )

    # --------------------------------------------------------
    # Create LangGraph state
    # --------------------------------------------------------

    initial_state = {
        "request": request.query,
        "cell_id": cell_id,
        "region": region,
        "messages": [
            HumanMessage(
                content=request.query
            )
        ],
    }

    # --------------------------------------------------------
    # Execute NetworkIQ
    # --------------------------------------------------------

    try:

        result = graph.invoke(
            initial_state
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"NetworkIQ execution failed: {exc}",
        )

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return InvestigationResponse(
        cell_id=result.get("cell_id"),
        region=result.get("region"),
        response=result.get(
            "final_response",
            "No response generated.",
        ),
    )