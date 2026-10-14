
from agents.intake import intake_agent
from agents.env_data import env_data_agent
from agents.regulations import regulations_agent
from agents.assessor import assessor_agent

description = (
    "A 50 MW solar farm covering approximately 120 acres "
    "near Pune, Maharashtra, involving land clearing, "
    "solar panel installation, and electrical infrastructure."
)

state = {
    "user_input": description,
    "project": None,
    "coordinates": None,
    "env_data": None,
    "regulations": None,
    "impact_ratings": None,
    "report": None,
    "errors": [],
}

# 1. Extract project details
state["project"] = intake_agent(description)

# 2. Collect environmental data
state.update(env_data_agent(state))

# 3. Search regulation documents
state.update(regulations_agent(state))

# 4. Assess impacts and generate the report
result = assessor_agent(state)

print("\nErrors:", result.get("errors", []))
print("\nImpact Ratings:")
print(result.get("impact_ratings"))
print("\nFinal Report:")
print(result.get("report", "Report generation failed"))
