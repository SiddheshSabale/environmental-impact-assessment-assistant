
from tools.reg_search import search_regulations


def regulations_agent(state: dict) -> dict:
    """Find potentially relevant regulation summaries for different projects."""

    project = state.get("project")

    if not project:
        return {
            "regulations": [],
            "errors": state.get("errors", []) + [
                "Regulations agent: project details are missing."
            ],
        }

    project_type = project.get("project_type", "")
    activities = project.get("key_activities", [])

    if isinstance(activities, str):
        activities = [activities]

    # Build searches from the project type and its individual activities.
    search_terms = []

    if project_type and project_type.strip().lower() != "unknown":
        search_terms.extend([
            project_type,
            f"environmental regulations for {project_type}",
            f"environmental impacts and pollution control for {project_type}",
        ])

    for activity in activities:
        if activity and activity.strip().lower() != "unknown":
            search_terms.extend([
                activity,
                f"environmental pollution control {activity}",
            ])

    results = []
    errors = list(state.get("errors", []))

    for term in search_terms:
        try:
            matches = search_regulations(term, top_k=5)
            results.extend(matches)
        except Exception as error:
            errors.append(
                f"Regulation search failed for '{term}': {error}"
            )

    # Remove duplicate source lines returned by overlapping searches.
    unique_results = []
    seen = set()

    for item in results:
        key = (item["source"], item["line_number"])

        if key not in seen:
            seen.add(key)
            unique_results.append(item)

    return {
        "regulations": unique_results,
        "errors": errors,
    }
