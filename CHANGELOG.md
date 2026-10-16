# Changelog

All notable changes to the Dunbar Veterinary Clinic Appointment Management System are recorded in this file. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [Semantic Versioning](https://semver.org/).

## [v1.1.0] - 2026-10-17

### Fixed

- Restored branch protection on `main`; all changes must now go through a feature branch and a reviewed pull request.
- Added continuous integration: GitHub Actions workflow runs the full pytest suite on every push and pull request.
- Added missing `.env.example` with illustrative values only; no real secrets are committed.

### Added

- `README.md` with clean-checkout reproduction steps (clone → venv → install → run → test).
- This `CHANGELOG.md` and a version tag for the release.

### Known Limitations (recorded in Confluence Change Log)

- Data is currently held in memory and is lost on restart. Migration to SQLite is planned for the next release (tracked as CR-02).
- Farm visit and property management are not implemented in this release; they remain in the Jira Product Backlog (see Confluence Handover page for deferral rationale).

## [v1.0.0] - 2026-10-09

### Added

- Sprint 1 and Sprint 2 delivery: client records, animal records linked to clients, appointment creation and cancellation, and query functions (client by ID, daily schedule, animal by ID).
- Unit test suite covering all delivered user stories (12 test cases).
