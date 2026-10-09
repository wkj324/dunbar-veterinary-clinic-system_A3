# Changelog

All notable changes to this project are documented here. Versioning follows
Semantic Versioning (MAJOR.MINOR.PATCH).

## [0.1.0] - 2026-09-25
### Added
- Client records: create, search, view, list.
- Animal records: create, list by client, search by name across all clients.
- Property records: create, list by client, remove.
- Appointment booking for two types:
  - in-clinic consultation with animal, 15-minute slot, timetable and
    room-conflict validation;
  - farm visit bound to a property with a duration in hours (> 0).
- Appointment change and cancel; cancelled records retained and distinct.
- Daily schedule view.
- Local SQLite persistence and offline operation.
- pytest test suite covering both appointment types and validation rules.
- GitHub Actions CI workflow, `.env.example`, `.gitignore`, README.
