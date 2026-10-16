# Dunbar Veterinary Clinic Appointment Management System

ISYS3001 Team5 - Sprint 1 Source Code

Team Members: Zhou Wenxin, Fan Wenqing, Wu Kejin

## Sprint 1 Scope

Core functions implemented:

1. Client record create and search
2. Animal records bound to client
3. Property records bound to client
4. Two types of appointments: in-clinic (15min fixed), farm visit (custom duration)
5. Create & cancel appointment
6. View daily appointment schedule

## Branch Strategy

- `main`: stable released code, protected; changes only via pull request
- Feature branches: `feature/client-model`, `feature/appointment-crud`
All feature code merged to main via Pull Request.

## Tests

Automated unit tests are located in /test folder.

## Requirements

- Python 3.x (developed on 3.12)
- pip

## Setup (clean checkout)

1. Clone the repository:
git clone https://github.com/wkj324/dunbar-veterinary-clinic-system_A3
cd dunbar-veterinary-clinic-system_A3
2. Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate
3. Install dependencies:
pip install pytest
4. Environment configuration:
copy .env.example .env
5. Run the verification (unit tests):
python -m pytest test/ -v

## CI

GitHub Actions runs pytest on every push and pull request to main
(see .github/workflows/ci.yml).

## Releases

See CHANGELOG.md and the Releases page. Current version: v1.1.0.

## Data and privacy

Only fictitious sample data may be used. No real client or patient data.
