"""Consulting timetable rules for in-clinic consultations.

Consultations are always one fixed 15-minute slot, in one of two consulting
rooms. Source of rules: Dunbar case-study paper documents.

  Mon / Wed / Fri : 08:30 - 17:15, last booking 17:15
  Tue / Thu      : consults only until 10:15
  Sat            : 08:00 - 11:00
  Sun            : closed
  Held slots     : 11:15 and 11:30 (surgery drop-offs) — never fill
"""


def _minutes(hhmm):
    h, m = (int(x) for x in hhmm.split(":"))
    return h * 60 + m


def weekday_range(weekday):
    """Return (start_min, end_min, held_set) for a Python weekday (Mon=0)."""
    if weekday in (0, 2, 4):          # Mon, Wed, Fri
        return _minutes("08:30"), _minutes("17:15"), {_minutes("11:15"), _minutes("11:30")}
    if weekday in (1, 3):             # Tue, Thu
        return _minutes("08:30"), _minutes("10:15"), set()
    if weekday == 5:                  # Sat
        return _minutes("08:00"), _minutes("11:00"), set()
    return None, None, None           # Sun closed


def is_valid_consult_slot(weekday, hhmm):
    """Return True if hhmm is a valid consult start slot on weekday."""
    m = _minutes(hhmm)
    start, end, held = weekday_range(weekday)
    if start is None:
        return False
    if m < start or m > end:
        return False
    if m in held:
        return False
    return m % 15 == 0


def slot_times(weekday):
    """List all valid consult start times for a weekday (HH:MM)."""
    start, end, held = weekday_range(weekday)
    if start is None:
        return []
    times = []
    m = start
    while m <= end:
        if m % 15 == 0 and m not in held:
            times.append(f"{m // 60:02d}:{m % 60:02d}")
        m += 1
    return times


def days_of_week():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def weekday_name(weekday):
    return days_of_week()[weekday]
