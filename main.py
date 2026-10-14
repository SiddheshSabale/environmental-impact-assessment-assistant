
from graph import build_graph


def main():
    print("\n=== Environmental Impact Assessment Assistant ===\n")

    description = input("Describe the proposed project: ").strip()

    if not description:
        print("Error: Project description cannot be empty.")
        return

    app = build_graph()

    initial_state = {
        "user_input": description,
        "project": None,
        "coordinates": None,
        "env_data": None,
        "regulations": None,
        "impact_ratings": None,
        "report": None,
        "errors": [],
    }

    print("\nProcessing project. Please wait...\n")

    result = app.invoke(initial_state)

    if result.get("errors"):
        print("Warnings / Errors:")
        for error in result["errors"]:
            print(f"- {error}")

    report = result.get("report")

    if report:
        print("\n" + "=" * 60)
        print("PRELIMINARY EIA REPORT")
        print("=" * 60)
        print(report)

        with open("eia_report.md", "w", encoding="utf-8") as file:
            file.write(report)

        print("\nReport saved to eia_report.md")
    else:
        print("\nReport generation failed. Check the errors above.")


if __name__ == "__main__":
    main()
