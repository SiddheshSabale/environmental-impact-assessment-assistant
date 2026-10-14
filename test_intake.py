
from agents.intake import intake_agent

description = (
    "A 50 MW solar farm covering approximately 120 acres "
    "near Pune, Maharashtra, involving land clearing, "
    "solar panel installation, and electrical infrastructure."
)

try:
    result = intake_agent(description)
    print("Intake agent successful")
    print(result)
except Exception as error:
    print(f"Intake agent failed: {error}")
