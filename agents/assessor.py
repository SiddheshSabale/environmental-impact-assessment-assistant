import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


IMPACT_RULES = [
    {
        "category": "Land and soil",
        "keywords": [
            "clearing", "excavation", "grading", "earthwork",
            "foundation", "construction", "land conversion",
        ],
        "impact": (
            "Soil disturbance, compaction, erosion, or possible "
            "contamination."
        ),
    },
    {
        "category": "Air quality",
        "keywords": [
            "clearing", "excavation", "construction", "machinery",
            "diesel", "vehicle", "transport", "installation",
            "emission", "boiler", "combustion", "processing",
            "dust", "burning",
        ],
        "impact": (
            "Potential dust, particulate matter, gaseous emissions, "
            "or equipment exhaust."
        ),
    },
    {
        "category": "Water resources",
        "keywords": [
            "clearing", "excavation", "earthwork", "runoff",
            "wastewater", "effluent", "water use", "chemical",
            "sewage", "drainage", "cooling water",
        ],
        "impact": (
            "Potential changes to water demand, runoff, drainage, "
            "or water quality."
        ),
    },
    {
        "category": "Biodiversity",
        "keywords": [
            "clearing", "vegetation", "tree", "forest",
            "habitat", "wildlife", "land conversion",
            "ecology", "biodiversity",
        ],
        "impact": (
            "Potential vegetation loss, habitat disturbance, "
            "or effects on wildlife."
        ),
    },
    {
        "category": "Waste management",
        "keywords": [
            "installation", "construction", "demolition", "waste",
            "battery", "packaging", "electrical infrastructure",
            "ash", "residue", "sludge", "disposal", "segregation",
        ],
        "impact": (
            "Potential generation of construction, operational, "
            "or hazardous waste."
        ),
    },
    {
        "category": "Noise",
        "keywords": [
            "construction", "machinery", "vehicle", "transport",
            "installation", "excavation", "electrical infrastructure",
            "boiler", "processing", "drilling",
        ],
        "impact": (
            "Potential noise and vibration during construction "
            "or operation."
        ),
    },
    {
        "category": "Land use and visual impact",
        "keywords": [
            "solar farm", "solar panel", "land clearing",
            "land conversion", "substation", "infrastructure",
            "residential", "highway", "factory", "plant",
            "building", "dam", "mine",
        ],
        "impact": (
            "Potential changes to existing land use, landscape, "
            "or local surroundings."
        ),
    },
    {
        "category": "Electrical safety",
        "keywords": [
            "electrical infrastructure", "transformer", "substation",
            "cabling", "power line", "grid interconnection",
            "electricity generation", "inverter",
        ],
        "impact": (
            "Potential electrical hazards associated with installation "
            "or operation."
        ),
    },
    {
        "category": "Public health and communities",
        "keywords": [
            "waste processing", "combustion", "emission", "sewage",
            "hazardous material", "traffic", "residential",
            "settlement", "industrial plant",
        ],
        "impact": (
            "Potential effects on nearby communities through pollution, "
            "traffic, or other project-related exposures."
        ),
    },
    {
        "category": "Traffic and transportation",
        "keywords": [
            "transport", "vehicle", "truck", "traffic",
            "material delivery", "waste collection", "road",
            "highway", "logistics",
        ],
        "impact": (
            "Potential increase in vehicle movements, congestion, "
            "and transport-related emissions."
        ),
    },
]


def screen_impacts(project: dict) -> dict:
    """Identify potential impacts using transparent keyword rules."""

    activities = project.get("key_activities", [])
    project_type = project.get("project_type", "")

    if isinstance(activities, str):
        activities = [activities]

    # Ignore empty or non-string activity values.
    activities = [
        activity
        for activity in activities
        if isinstance(activity, str) and activity.strip()
    ]

    project_type = (
        project_type if isinstance(project_type, str) else ""
    )

    impacts = []

    for rule in IMPACT_RULES:
        matched_activities = [
            activity
            for activity in activities
            if any(
                keyword in activity.lower()
                for keyword in rule["keywords"]
            )
        ]

        project_type_match = any(
            keyword in project_type.lower()
            for keyword in rule["keywords"]
        )

        if matched_activities or project_type_match:
            triggers = matched_activities or [
                f"Project type: {project_type}"
            ]

            impacts.append({
                "category": rule["category"],
                "potential_impact": rule["impact"],
                "triggering_activities": triggers,
                "status": "Requires further investigation",
                "method": "Keyword-based preliminary screening",
            })

    if not impacts:
        impacts.append({
            "category": "General environmental screening",
            "potential_impact": (
                "The rule-based screening did not identify specific "
                "impacts. Further project-specific assessment is needed."
            ),
            "triggering_activities": activities,
            "status": "Requires further investigation",
            "method": "No matching keywords found",
        })

    return {
        "assessment_type": "Preliminary rule-based screening",
        "impacts": impacts,
        "limitations": [
            "Keyword matching may miss relevant project-specific impacts.",
            "Impact severity, probability, and significance are not quantified.",
            "Site-specific baseline surveys may be unavailable.",
            "Identified impacts require project-specific verification.",
        ],
    }


def assessor_agent(state: dict) -> dict:
    """Screen impacts and generate a project-specific preliminary EIA report."""

    project = state.get("project")
    errors = list(state.get("errors", []))

    if not project:
        return {
            "errors": errors + [
                "Assessor: project details are missing."
            ]
        }

    impact_ratings = screen_impacts(project)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "impact_ratings": impact_ratings,
            "errors": errors + [
                "Assessor: GROQ_API_KEY is missing from .env."
            ],
        }

    env_data = state.get("env_data") or {}
    regulations = state.get("regulations") or []

    try:
        llm = ChatGroq(
            model=MODEL_NAME,
            temperature=0,
            api_key=api_key,
            max_tokens=8000,
        )

        prompt = f"""
Prepare a preliminary Environmental Impact Assessment (EIA) report
for the specific proposed project described below.

PROJECT DETAILS:
{project}

ENVIRONMENTAL DATA:
{env_data}

LOCAL REGULATION SEARCH RESULTS:
{regulations}

RULE-BASED IMPACT SCREENING:
{impact_ratings}

REQUIRED REPORT SECTIONS:

1. Project overview
2. Environmental observations and data limitations
3. Potential environmental impacts
4. Regulation search findings and verification needs
5. Preliminary mitigation recommendations
6. Missing information and next steps
7. Disclaimer

PROJECT-SPECIFIC ASSESSMENT INSTRUCTIONS:

- Adapt the assessment to the actual project type and activities.
- Use the rule-based screening as a starting point, not as a complete
  list of all possible impacts.
- Identify additional plausible impacts relevant to the project,
  while clearly distinguishing them from rule-based screening results.
- Consider air emissions, water demand, wastewater, soil, biodiversity,
  noise, waste, traffic, energy, occupational safety, public health,
  and communities where relevant.
- Select only categories relevant to the project.
- For industrial or waste-processing projects, consider process
  emissions, wastewater, hazardous materials, residues, and waste
  handling where supported by the project description.
- For residential projects, consider construction impacts, water
  demand, sewage, solid waste, traffic, and land-use changes where relevant.
- For roads and transport projects, consider land disturbance,
  drainage, habitat fragmentation, noise, and vehicle emissions.
- For energy projects, consider construction, land use, waste,
  emissions where applicable, and electrical infrastructure.
- Explain why each potential impact is relevant and identify the
  activities that could cause it.
- Do not claim that a potential impact has been measured or confirmed
  unless the supplied evidence establishes that fact.
- Distinguish observed or supplied information from potential impacts,
  assumptions, limitations, and recommendations.

STRICT EVIDENCE RULES:

- Do not invent project details, measurements, timestamps, coordinates,
  monitoring stations, or environmental observations.
- Do not assume actual land use, nearby water bodies, protected species,
  settlements, or site conditions.
- Describe weather and air-quality readings as retrieved snapshots,
  not verified site-specific baseline measurements.
- Do not invent legislation, legal sections, thresholds, permits,
  authorities, clearance requirements, or compliance conclusions.
- Mention a specific law, rule, legal category, or threshold only if
  it appears in the supplied local regulation search results.
- Do not cite legislation from your own knowledge if it is absent from
  the supplied regulation search results. Instead, state:
  "Other potentially applicable laws require separate verification."
- Do not name or give examples of any additional laws or rules that are
  absent from the supplied regulation search results, including in the
  report's notes, recommendations, or disclaimer. Use only the generic
  verification statement above.
- Do not assign legal categories such as Category A, B, or C unless
  that exact classification is supported by the supplied evidence.
- Do not claim that a particular clearance, permit, or approval is
  required unless the supplied evidence supports that conclusion.
- Treat regulation results as local keyword-search matches, not as
  verified legal evidence or a complete list of applicable laws.
- If no regulation matches are supplied, explicitly state that the
  search returned no matches. Do not infer that no laws apply.
- Do not introduce numerical project facts, measurements, impact scores,
  legal thresholds, or classifications unless supported by the project
  input or supplied data.
- Do not compare environmental readings against WHO guidelines,
  regulatory limits, or other external guidelines unless those
  specific reference values are included in the supplied evidence.
- Do not describe an environmental reading as safe, unsafe, compliant,
  or non-compliant without sufficient supplied evidence and context.
- Do not invent numerical impact scores or claim that severity,
  probability, or significance has been quantitatively assessed.
- Explain that geocoded coordinates may identify a landmark rather
  than the actual project boundary.
- Do not infer that weather or air-quality data represents the project
  site if the exact site location has not been confirmed.
- Identify missing information rather than filling gaps with assumptions.
- Label mitigation measures as preliminary recommendations, not
  confirmed legal requirements.
- State that this is not a statutory EIA, legal opinion, environmental
  clearance, or compliance determination.

REPORT QUALITY:

- Use clear Markdown headings and tables where useful.
- Keep the report specific to the supplied project.
- Avoid repeating the same information across sections.
- Explain the limitations of the available evidence.
- Do not fabricate references or citations.
- Do not claim that a regulation search is exhaustive.
- Keep all seven required sections in the final report.
- Use section numbers for report organization, but do not introduce
  unsupported numerical findings or legal classifications.

Return only the completed Markdown report.
"""

        response = llm.invoke([
            SystemMessage(
                content=(
                    "You prepare preliminary environmental screening "
                    "reports for different types of proposed development "
                    "projects. Adapt the assessment to the supplied "
                    "project rather than assuming it is a solar farm "
                    "or any other fixed project type. Evidence accuracy "
                    "is more important than completeness. Never invent "
                    "facts, legislation, numerical findings, or legal "
                    "conclusions. Clearly distinguish supplied evidence, "
                    "potential impacts, limitations, and recommendations. "
                    "Follow every evidence restriction in the user's "
                    "instructions."
                )
            ),
            HumanMessage(content=prompt),
        ])

        if response.response_metadata.get("finish_reason") == "length":
            errors.append(
                "Assessor: report was truncated by the token limit."
            )

        if not isinstance(response.content, str):
            raise ValueError("Unexpected report response format.")

        report = response.content.strip()

        if not report:
            raise ValueError("The model returned an empty report.")

        return {
            "impact_ratings": impact_ratings,
            "report": report,
            "errors": errors,
        }

    except Exception as error:
        return {
            "impact_ratings": impact_ratings,
            "errors": errors + [
                f"Report generation failed: {error}"
            ],
        }