
from typing import TypedDict, Optional


class ProjectInfo(TypedDict):
    project_type: str
    location_text: str
    size_description: str
    key_activities: list[str]


class Coordinates(TypedDict):
    lat: float
    lon: float


class EIAState(TypedDict):
    user_input: str
    project: Optional[ProjectInfo]
    coordinates: Optional[Coordinates]
    env_data: Optional[dict]
    regulations: Optional[list[dict]]
    impact_ratings: Optional[dict]
    report: Optional[str]
    errors: list[str]
