
from graph import build_graph


def test_complete_workflow():
    app = build_graph()

    initial_state = {
        "user_input": (
            "A 50 MW solar farm covering 120 acres near Pune, "
            "Maharashtra, involving land clearing, solar panel "
            "installation, and electrical infrastructure."
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

    assert result.get("project"), "Project details were not extracted"
    assert result.get("impact_ratings"), "Impact screening did not run"
    assert result.get("report"), "Report was not generated"
    assert result.get("errors", []) == [], result.get("errors")

    print("Workflow test passed!")
    print("Project:", result["project"]["project_type"])
    print("Impact categories:", len(result["impact_ratings"]["impacts"]))
    print("Report generated:", bool(result["report"]))


if __name__ == "__main__":
    test_complete_workflow()
