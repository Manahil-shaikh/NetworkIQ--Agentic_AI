from langchain_core.messages import HumanMessage

from networkiq.agents.agent_graph import build_agent_graph
from networkiq.agents.request_parser import parse_request


def main() -> None:

    # --------------------------------------------------------
    # User request
    # --------------------------------------------------------

    request = (
        "Investigate ISB_002 in Islamabad "
        "and determine whether there are network "
        "performance problems."
    )

    # --------------------------------------------------------
    # Parse request
    # --------------------------------------------------------

    parsed = parse_request(request)

    print("\nParsed request:")
    print(parsed)

    if not parsed.get("cell_id"):
        print("Could not identify a cell ID.")
        return

    # --------------------------------------------------------
    # Build initial LangGraph state
    # --------------------------------------------------------

    initial_state = {
        "request": request,
        "cell_id": parsed["cell_id"],
        "region": parsed["region"],
        "messages": [
            HumanMessage(
                content=request
            )
        ],
    }

    # --------------------------------------------------------
    # Build graph
    # --------------------------------------------------------

    graph = build_agent_graph()

    # --------------------------------------------------------
    # Execute graph
    # --------------------------------------------------------

    result = graph.invoke(
        initial_state
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("FINAL NETWORKIQ RESULT")
    print("=" * 70)

    print(
        result.get(
            "final_response",
            "No final response generated.",
        )
    )


if __name__ == "__main__":
    main()