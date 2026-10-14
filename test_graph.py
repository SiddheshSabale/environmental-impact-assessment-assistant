
from graph import build_graph

app = build_graph()

initial_state = {
    "user_input": (
        "A 50 MW solar farm covering 120 acres near Pune, Maharashtra, "
        "involving land clearing, solar panel installation, "
        "and electrical infrastructure."
    ),
    "project": None,
    "coordinates": None,
    "env_data": None,
    "regulations": None,
    "impact_ratings": None,
    "report": None,
    "errors": [],
}

result = app.invoke(initial_state)

print("Errors:", result.get("errors", []))
print("\nProject:", result.get("project"))
print("\nImpact Ratings:", result.get("impact_ratings"))
print("\nFinal Report:\n", result.get("report"))
