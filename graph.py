
from langgraph.graph import StateGraph, START, END

from state import EIAState
from agents.intake import intake_agent
from agents.env_data import env_data_agent
from agents.regulations import regulations_agent
from agents.assessor import assessor_agent


def intake_node(state: EIAState) -> dict:
    try:
        project = intake_agent(state["user_input"])
        return {"project": project}
    except Exception as error:
        return {
            "errors": state.get("errors", [])
            + [f"Intake agent failed: {error}"]
        }


def env_data_node(state: EIAState) -> dict:
    return env_data_agent(state)


def regulations_node(state: EIAState) -> dict:
    return regulations_agent(state)


def assessor_node(state: EIAState) -> dict:
    return assessor_agent(state)


def route_after_intake(state: EIAState) -> str:
    if state.get("project") and not state.get("errors"):
        return "env_data"
    return "end"


def build_graph():
    workflow = StateGraph(EIAState)

    workflow.add_node("intake", intake_node)
    workflow.add_node("env_data", env_data_node)
    workflow.add_node("regulations", regulations_node)
    workflow.add_node("assessor", assessor_node)

    workflow.add_edge(START, "intake")

    workflow.add_conditional_edges(
        "intake",
        route_after_intake,
        {
            "env_data": "env_data",
            "end": END,
        },
    )

    workflow.add_edge("env_data", "regulations")
    workflow.add_edge("regulations", "assessor")
    workflow.add_edge("assessor", END)

    return workflow.compile()
