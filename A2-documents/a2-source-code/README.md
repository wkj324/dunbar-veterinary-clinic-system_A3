# Dunbar Veterinary Clinic — Appointment System

A small, offline-first web application for a mixed-practice country veterinary
clinic. Manages clients, animals, properties and two kinds of appointment:
in-clinic consultations and farm visits.

**Note for the assessor:** this project uses fictitious/sample data only. No
real client data and no secrets are stored or committed. The application runs
fully offline — it has no runtime dependency on the internet.

## Features

- Client, animal and property records (create, search, list)
- Two appointment types with domain validation:
  - **In-clinic consultation**: one animal, one fixed 15-minute slot, one of
    two consulting rooms, must land on the consulting timetable, no double
    booking in the same room.
  - **Farm visit**: bound to a property, start time plus an estimated
    duration in hours (must be greater than zero).
- Change and cancel appointments — cancelled records are retained and clearly
  distinguished from live ones.
- Daily schedule view.
- Local SQLite persistence (data survives a restart).

## Prerequisites

- Python 3.10 or newer
- pip

## Setup and run (from a clean checkout)

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd dunbar_vet_app

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Prepare environment config
cp .env.example .env          # Windows:  copy .env.example .env

# 5. Initialise the database and start the app
python app.py

# 6. Open in your browser
#    http://127.0.0.1:5000
```

## Running the tests

```bash
pytest -v
```

## Repository structure

```
dunbar_vet_app/
├── app.py          # Flask application and routes
├── db.py           # SQLite schema and connection helpers
├── models.py       # domain logic and data operations
├── timetable.py    # consulting timetable rules
├── templates/      # Jinja2 HTML templates
├── tests/          # pytest test suite
├── requirements.txt
├── .env.example    # environment template (commit this)
├── .gitignore
├── CHANGELOG.md
└── .github/workflows/ci.yml
```

## Configuration

All configuration is read from environment variables (see `.env.example`):

- `SECRET_KEY` — Flask session secret (dev value only, never committed).
- `DATABASE_PATH` — path to the SQLite database file.

## Branching

- Feature branches follow `feature/<feature-name>` and are merged via pull
  requests with review.

###feature/vet-staff
- Implemented vet staff information and schedule management functions
- Implemented animal record management functions
- Implemented appointment booking and schedule management functions
 main

