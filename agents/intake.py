
import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def intake_agent(user_input: str) -> dict:
    """Extract structured project information from user input."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not user_input.strip():
        raise ValueError("Project description cannot be empty.")

    llm = ChatGroq(
        model=MODEL_NAME,
        temperature=0,
        api_key=api_key,
    )

    messages = [
        SystemMessage(
            content=(
                "You are an environmental project intake agent. "
                "Extract project details from the user's description. "
                "Return ONLY valid JSON with these fields: "
                "project_type, location_text, size_description, "
                "key_activities. "
                "key_activities must be a list of strings. "
                "Use 'unknown' for missing text fields and an empty "
                "list for missing activities. Never invent details."
            )
        ),
        HumanMessage(content=user_input),
    ]

    response = llm.invoke(messages)
    content = response.content

    if not isinstance(content, str):
        raise ValueError("The LLM returned an unexpected response format.")

    try:
        project = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Intake agent returned invalid JSON: {content}"
        ) from exc

    required_fields = {
        "project_type",
        "location_text",
        "size_description",
        "key_activities",
    }

    if not isinstance(project, dict) or not required_fields.issubset(project):
        raise ValueError("Intake agent returned incomplete project data.")

    if not isinstance(project["key_activities"], list):
        raise ValueError("key_activities must be a list.")

    return {
        "project_type": str(project["project_type"]),
        "location_text": str(project["location_text"]),
        "size_description": str(project["size_description"]),
        "key_activities": [
            str(activity) for activity in project["key_activities"]
        ],
    }
