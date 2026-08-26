# from langchain_core.messages import HumanMessage, SystemMessage

# from networkiq.llm.ollama import create_llm
# from networkiq.llm.prompts import SYSTEM_PROMPT
# from networkiq.tools.network_tools import (
#     get_cell_info,
#     get_network_kpis,
#     get_recent_incidents,
# )


# def main() -> None:

#     llm = create_llm()

#     tools = [
#         get_network_kpis,
#         get_cell_info,
#         get_recent_incidents,
#     ]

#     llm_with_tools = llm.bind_tools(tools)

#     messages = [
#         SystemMessage(content=SYSTEM_PROMPT),
#         HumanMessage(
#             content=(
#                 "Investigate cell ISB_002. "
#                 "Start by retrieving its network KPIs."
#             )
#         ),
#     ]

#     response = llm_with_tools.invoke(messages)

#     print("\nLLM response:")
#     print(response)

#     print("\nTool calls:")
#     print(response.tool_calls)


# if __name__ == "__main__":
#     main()


from networkiq.llm.ollama import create_structured_llm
from networkiq.llm.prompts import RCA_PROMPT


def main() -> None:

    llm = create_structured_llm()

    evidence = """
    Cell: ISB_002

    PRB utilization: 96%
    Active users: 450
    DL throughput: 14 Mbps
    UL throughput: 5 Mbps
    Call drop rate: 4.1%
    Handover success rate: 93%

    Detected anomalies:
    - High PRB utilization
    - High call drop rate
    - Low handover success rate
    """

    prompt = RCA_PROMPT.format(
        evidence=evidence
    )

    result = llm.invoke(prompt)

    print("\nStructured RCA:")
    print(result)

    print("\nPython type:")
    print(type(result))


if __name__ == "__main__":
    main()