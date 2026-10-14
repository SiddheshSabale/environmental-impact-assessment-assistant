# Environmental Impact Assessment Assistant

An AI-powered, multi-agent system that generates preliminary Environmental Impact Assessment (EIA) reports for proposed development projects. The system combines Large Language Models (LLMs), environmental data retrieval, local regulation searches, and rule-based impact screening to identify potential environmental risks and recommend preliminary mitigation measures.

## Problem Statement

Environmental impact assessment requires analysing project activities, environmental conditions, applicable regulations, and potential risks. Performing an initial assessment manually can be time-consuming.

This project aims to simplify preliminary environmental screening through a multi-agent workflow that collects project information, retrieves environmental data, searches relevant regulation summaries, identifies potential impacts, and generates a structured report.

## Key Features

- **Multi-agent architecture:** Uses LangGraph to orchestrate specialised agents.
- **Project information extraction:** Extracts project type, location, size, and key activities from natural-language input.
- **Environmental data retrieval:** Uses geocoding and Open-Meteo APIs to retrieve environmental snapshots.
- **Regulation search:** Searches local summaries of selected Indian environmental legislation.
- **Impact screening:** Applies transparent keyword-based rules to identify potential environmental impacts.
- **AI-generated assessment:** Uses a Groq-hosted LLM to prepare a project-specific preliminary EIA report.
- **Mitigation recommendations:** Suggests preliminary measures based on the supplied project information and identified risks.
- **Markdown report generation:** Displays the assessment and saves the generated report as `eia_report.md`.
- **Error handling:** Records errors encountered during agent execution and tool calls.

## System Architecture

The application follows a sequential multi-agent workflow.

```text
User Input
    |
    v
Intake Agent
    |
    | Extract project details
    v
Environmental Data Agent
    |
    | Geocode location and retrieve data
    v
Regulations Agent
    |
    | Search local regulation summaries
    v
Assessor Agent
    |
    | Rule-based screening + LLM analysis
    v
Preliminary EIA Report
    |
    v
Save as eia_report.md
```

### Agents

| Agent | Responsibility |
|---|---|
| Intake Agent | Extracts structured project information from natural-language input |
| Environmental Data Agent | Retrieves location-related environmental data |
| Regulations Agent | Searches local summaries for potentially relevant environmental regulations |
| Assessor Agent | Identifies potential impacts, combines rule-based screening with LLM analysis, and generates the report |

### Supporting Tools

- **Geocoding Tool:** Converts a location description into geographic coordinates.
- **Climate and Air Quality Tool:** Retrieves available weather and air-quality data from Open-Meteo.
- **Regulation Search Tool:** Searches local environmental regulation summaries using keyword matching.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| LangGraph | Agent orchestration and workflow management |
| LangChain | LLM integration |
| Groq API | Language model inference |
| Python-dotenv | Environment variable management |
| Pydantic | Structured data validation, where used |
| Requests | HTTP requests to external APIs |
| Open-Meteo | Environmental data retrieval |
| Nominatim / OpenStreetMap | Location geocoding |
| Pytest | Workflow testing |
| Git and GitHub | Version control and project submission |

## Project Structure

```text
Environmental Impact Assessment Assistant/
│
├── agents/
│   ├── __init__.py
│   ├── intake.py
│   ├── env_data.py
│   ├── regulations.py
│   └── assessor.py
│
├── tools/
│   ├── __init__.py
│   ├── geo.py
│   ├── climate.py
│   └── reg_search.py
│
├── data/
│   └── regulations/
│       ├── eia_notification_2006.md
│       ├── water_act_1974.md
│       └── air_act_1981.md
│
├── state.py
├── graph.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── eia_report.md
│
└── test_*.py
```

## Installation and Setup

### Prerequisites

- Python 3.11 or later, compatible with the installed dependencies
- pip
- A Groq API key
- Internet connectivity for the external APIs

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Environmental Impact Assessment Assistant"
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Replace `your_groq_api_key` with your own Groq API key.

**Security note:** Never upload your `.env` file or expose your API key in source code or screenshots. Keep `.env` excluded through `.gitignore`.

## How to Run the Project

Run the application from the project root:

```bash
python main.py
```

When prompted, enter a description of the proposed project, including its location, approximate size, and major activities.

### Example Input

```text
A proposed 20 MW waste-to-energy plant near Mumbai,
Maharashtra, India, covering approximately 25 acres.
Activities include waste segregation, waste processing,
boiler installation, air pollution control, wastewater
treatment, ash disposal, and electricity generation.
Identify potential environmental impacts and recommend
preliminary mitigation measures.
```

### Expected Output

The application processes the input through its agent workflow and generates a preliminary report containing:

1. Project overview
2. Environmental observations and data limitations
3. Potential environmental impacts
4. Regulation search findings and verification needs
5. Preliminary mitigation recommendations
6. Missing information and next steps
7. Disclaimer

The generated report is saved as:

```text
eia_report.md
```

The application can be given different project descriptions, such as residential developments, renewable energy projects, roads, industrial facilities, or waste-processing plants. Assessment quality depends on the project details supplied, the available environmental data, the local regulation summaries, and the model response.

## Testing

The project includes test scripts for individual components and the complete workflow.

Run the complete workflow test suite with:

```bash
pytest -v
```

To run individual test scripts, use the corresponding filenames, for example:

```bash
python test_geo.py
python test_climate.py
python test_reg_search.py
python test_intake.py
python test_env_data.py
python test_regulations_agent.py
python test_assessor.py
python test_impact_rules.py
python test_workflow.py
```

Run these commands only for test files present in the repository.

### Current Test Status

The complete workflow test has passed successfully.

- Test result: **1 passed**
- Execution time: Approximately 78 seconds
- Verified workflow: Project intake, agent orchestration, and report generation

The current `pytest -v` configuration collects one automated test. The other component scripts can be executed individually, but they are not necessarily collected as automated pytest tests.

## Limitations

- **Preliminary assessment only:** The system does not replace a professional or statutory Environmental Impact Assessment.
- **Environmental data limitations:** Retrieved weather and air-quality readings are snapshots and may not represent actual conditions at the project site.
- **Geocoding limitations:** A geocoded location may identify a landmark or general area rather than the exact project boundary.
- **Regulation search limitations:** Regulation findings come from local summaries and keyword matching. They are not a comprehensive search of current legislation.
- **Rule-based screening limitations:** Keyword matching may miss relevant impacts or identify broad categories that require further investigation.
- **LLM limitations:** Generated assessments may contain inaccuracies or unsupported conclusions and must be independently reviewed.
- **No quantitative risk assessment:** The current implementation does not establish scientifically validated impact severity, probability, or significance scores.
- **Site-specific information:** Field surveys, project designs, baseline measurements, and expert validation may be required for a reliable assessment.

## Future Enhancements

- Integrate authoritative and regularly updated environmental regulations.
- Improve impact detection through structured environmental knowledge bases.
- Add severity, likelihood, and significance assessment using a documented methodology.
- Integrate verified site-specific environmental and geospatial datasets.
- Introduce human review and approval before finalising reports.
- Develop a web interface for project submission and report viewing.
- Expand automated tests to cover individual agents, tools, error conditions, and different project types.

## Disclaimer

This project is intended for academic and preliminary environmental screening purposes only. It does not constitute a statutory EIA report, legal opinion, environmental clearance, or determination of regulatory compliance. All findings, potential impacts, and recommendations require appropriate verification by qualified environmental professionals and relevant authorities.

## Academic Project

**Project Title:** Environmental Impact Assessment Assistant  
**Subject:** Agentic Artificial Intelligence  
**Architecture:** Multi-agent workflow using LangGraph  
**Language:** Python

Developed as an individual academic project.
