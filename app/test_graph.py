from networkiq.agents.graph import build_graph


def main() -> None:

    graph = build_graph()

    initial_state = {
        "request": "Why is ISB_002 performing badly?",
        "cell_id": "ISB_002",
        "region": "Islamabad",
    }

    result = graph.invoke(initial_state)

    print("\nFinal state:")
    print(result)


if __name__ == "__main__":
    main()