# from networkiq.tools.network_tools import (
#     get_cell_info,
#     get_network_kpis,
#     get_recent_incidents,
# )


# def main() -> None:

#     tools = [
#         get_network_kpis,
#         get_cell_info,
#         get_recent_incidents,
#     ]

#     for tool in tools:

#         print("\n" + "=" * 60)
#         print(f"Tool: {tool.name}")
#         print(f"Description:\n{tool.description}")
#         print(f"Arguments:\n{tool.args}")


# if __name__ == "__main__":
#     main()


from networkiq.tools.network_tools import (
    get_cell_info,
    get_network_kpis,
    get_recent_incidents,
)


def main() -> None:

    print("\n=== KPI TOOL ===")

    result = get_network_kpis.invoke(
        {
            "cell_id": "ISB_002",
        }
    )

    print(result)

    print("\n=== CELL INFO TOOL ===")

    result = get_cell_info.invoke(
        {
            "cell_id": "ISB_002",
        }
    )

    print(result)

    print("\n=== INCIDENT TOOL ===")

    result = get_recent_incidents.invoke(
        {
            "cell_id": "ISB_002",
        }
    )

    print(result)


if __name__ == "__main__":
    main()