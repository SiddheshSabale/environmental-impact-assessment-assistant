
from agents.assessor import screen_impacts

project = {
    "project_type": "solar farm",
    "location_text": "near Pune, Maharashtra",
    "size_description": "50 MW, 120 acres",
    "key_activities": [
        "land clearing",
        "solar panel installation",
        "electrical infrastructure",
    ],
}

result = screen_impacts(project)

for impact in result["impacts"]:
    print(
        f'{impact["category"]}: '
        f'{impact["status"]}'
    )

print("\nTotal impact categories:", len(result["impacts"]))
