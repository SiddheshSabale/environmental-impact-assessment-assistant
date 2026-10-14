
import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq

from tools.geo import geocode_location
from tools.climate import get_climate_data

load_dotenv()


@tool
def geocode_tool(location: str) -> dict:
    """Convert a place description into latitude, longitude and display name."""
    return geocode_location(location)


@tool
def climate_tool(latitude: float, longitude: float) -> dict:
    """Get weather and air-quality data for the given coordinates."""
    return get_climate_data(latitude, longitude)


TOOLS = {
    "geocode_tool": geocode_tool,
    "climate_tool": climate_tool,
}


def run_tool_loop(llm, messages, max_steps=5):
    """Execute LLM-requested tool calls and collect their results."""

    collected = {}

    for _ in range(max_steps):
        ai_message = llm.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            break

        for call in ai_message.tool_calls:
            # Debug output to verify which tools the LLM requests.
            print("TOOL CALL:", call["name"], call["args"])

            tool_name = call["name"]

            if tool_name not in TOOLS:
                raise ValueError(f"Unknown tool requested: {tool_name}")

            result = TOOLS[tool_name].invoke(call["args"])
            collected[tool_name] = result

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=call["id"],
                )
            )

    return collected


def env_data_agent(state: dict) -> dict:
    """Collect location-related environmental data using LLM tool calling."""

    project = state.get("project")

    if not project:
        return {
            "errors": state.get("errors", []) + [
                "Environmental data agent: project details are missing."
            ]
        }

    location = project.get("location_text", "")

    if not location or location.strip().lower() == "unknown":
        return {
            "errors": state.get("errors", []) + [
                "Environmental data agent: project location is missing."
            ]
        }

    try:
        model_name = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b",
        )
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from .env.")

        llm = ChatGroq(
            model=model_name,
            temperature=0,
            api_key=api_key,
        )

        llm = llm.bind_tools(list(TOOLS.values()))

        messages = [
            SystemMessage(
                content=(
                    "You collect environmental data for a project site. "
                    "Pass only the place name to geocode_tool, without "
                    "words like 'near' or 'around'. For example, use "
                    "'Mumbai, Maharashtra, India' instead of "
                    "'near Mumbai, Maharashtra, India'. "
                    "First call geocode_tool with the supplied location. "
                    "After receiving its result, call climate_tool using "
                    "the returned latitude and longitude. "
                    "Do not invent coordinates or tool results. "
                    "Stop after both tools have returned results."
                )
            ),
            HumanMessage(
                content=f"Project location: {location}"
            ),
        ]

        collected = run_tool_loop(llm, messages)

        if "geocode_tool" not in collected:
            raise ValueError(
                "LLM did not call geocode_tool successfully."
            )

        if "climate_tool" not in collected:
            raise ValueError(
                "LLM did not call climate_tool successfully."
            )

        geo = collected["geocode_tool"]
        climate = collected["climate_tool"]

        if not isinstance(geo, dict):
            raise ValueError(
                "Geocoding tool returned an unexpected result."
            )

        if not isinstance(climate, dict):
            raise ValueError(
                "Climate tool returned an unexpected result."
            )

        if "latitude" not in geo or "longitude" not in geo:
            raise ValueError(
                "Geocoding result is missing latitude or longitude."
            )

        return {
            "coordinates": {
                "lat": geo["latitude"],
                "lon": geo["longitude"],
            },
            "env_data": {
                **climate,
                "resolved_location": geo.get(
                    "display_name",
                    location,
                ),
            },
        }

    except Exception as error:
        return {
            "errors": state.get("errors", []) + [
                f"Environmental data agent failed: {error}"
            ]
        }
