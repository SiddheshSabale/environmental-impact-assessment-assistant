
from agents.env_data import env_data_agent

state = {
    "user_input": "A solar farm near Pune",
    "project": {
        "project_type": "solar farm",
        "location_text": "Pune, Maharashtra, India",
        "size_description": "50 MW, 120 acres",
        "key_activities": ["land clearing", "panel installation"],
    },
    "coordinates": None,
    "env_data": None,
    "regulations": None,
    "impact_ratings": None,
    "report": None,
    "errors": [],
}

result = env_data_agent(state)

print(result)
