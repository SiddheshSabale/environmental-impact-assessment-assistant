
from agents.regulations import regulations_agent

state = {
    "user_input": "A 50 MW solar farm near Pune",
    "project": {
        "project_type": "solar farm",
        "location_text": "Pune, Maharashtra, India",
        "size_description": "50 MW, 120 acres",
        "key_activities": [
            "land clearing",
            "solar panel installation",
            "electrical infrastructure",
        ],
    },
    "coordinates": None,
    "env_data": None,
    "regulations": None,
    "impact_ratings": None,
    "report": None,
    "errors": [],
}

result = regulations_agent(state)

print("Regulations Agent Result:")
print(result)
