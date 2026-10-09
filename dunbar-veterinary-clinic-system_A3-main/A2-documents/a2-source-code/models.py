"""Domain logic and data operations for the Dunbar clinic application.

Holds the genuine domain rules for the two appointment kinds:
  - in-clinic consultation: one animal, fixed 15-minute slot, a room,
    must land on the consulting timetable and not conflict with another
    booking in the same room.
  - farm visit: bound to a property (not an animal), start time plus an
    estimated duration in hours (greater than zero).
"""

import datetime

import timetable

# --------------------------------------------------------------------------
# Clients
# --------------------------------------------------------------------------
def create_client(db, name, phone, email="", address="", client_type="household"):
    cur = db.execute(
        "INSERT INTO clients (name, phone, email, address, client_type, active) "
        "VALUES (?,?,?,?,?,1)", (name, phone, email, address, client_type))
    db.commit()
    return cur.lastrowid


def get_client(db, client_id):
    return db.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()


def search_clients(db, q):
    if q:
        like = f"%{q}%"
        return db.execute(
            "SELECT * FROM clients WHERE active=1 AND (name LIKE ? OR phone LIKE ?) "
            "ORDER BY name", (like, like)).fetchall()
    return db.execute("SELECT * FROM clients WHERE active=1 ORDER BY name").fetchall()


def all_clients(db):
    return db.execute("SELECT * FROM clients WHERE active=1 ORDER BY name").fetchall()


def set_client_active(db, client_id, active):
    db.execute("UPDATE clients SET active=? WHERE id=?", (1 if active else 0, client_id))
    db.commit()


# --------------------------------------------------------------------------
# Animals
# --------------------------------------------------------------------------
def create_animal(db, client_id, name, species, breed=""):
    cur = db.execute(
        "INSERT INTO animals (client_id, name, species, breed) VALUES (?,?,?,?)",
        (client_id, name, species, breed))
    db.commit()
    return cur.lastrowid


def list_animals_for_client(db, client_id):
    return db.execute("SELECT * FROM animals WHERE client_id=? ORDER BY name",
                      (client_id,)).fetchall()


def search_animals(db, q):
    if q:
        like = f"%{q}%"
        return db.execute(
            "SELECT a.*, c.name AS owner_name FROM animals a JOIN clients c "
            "ON a.client_id = c.id WHERE a.name LIKE ? ORDER BY a.name",
            (like,)).fetchall()
    return db.execute(
        "SELECT a.*, c.name AS owner_name FROM animals a JOIN clients c "
        "ON a.client_id = c.id ORDER BY a.name").fetchall()


def get_animal(db, animal_id):
    return db.execute("SELECT * FROM animals WHERE id=?", (animal_id,)).fetchone()


# --------------------------------------------------------------------------
# Properties
# --------------------------------------------------------------------------
def create_property(db, client_id, name, locality, access_notes=""):
    cur = db.execute(
        "INSERT INTO properties (client_id, name, locality, access_notes) "
        "VALUES (?,?,?,?)", (client_id, name, locality, access_notes))
    db.commit()
    return cur.lastrowid


def list_properties_for_client(db, client_id):
    return db.execute("SELECT * FROM properties WHERE client_id=? ORDER BY name",
                      (client_id,)).fetchall()


def get_property(db, property_id):
    return db.execute("SELECT * FROM properties WHERE id=?", (property_id,)).fetchone()


def remove_property(db, property_id):
    db.execute("DELETE FROM properties WHERE id=?", (property_id,))
    db.commit()


# --------------------------------------------------------------------------
# Appointments
# --------------------------------------------------------------------------
def _parse_day(day):
    try:
        return datetime.date.fromisoformat(day)
    except (TypeError, ValueError):
        return None


def _resolve_owner_names(db, row):
    d = dict(row)
    d["client"] = dict(db.execute("SELECT * FROM clients WHERE id=?",
                                  (d["client_id"],)).fetchone())
    if d.get("animal_id"):
        d["animal"] = dict(db.execute("SELECT * FROM animals WHERE id=?",
                                      (d["animal_id"],)).fetchone())
    if d.get("property_id"):
        d["property"] = dict(db.execute("SELECT * FROM properties WHERE id=?",
                                        (d["property_id"],)).fetchone())
    return d


def book_consultation(db, client_id, animal_id, day, time, room, reason):
    """Return None on success, else an error message string."""
    if not animal_id:
        return "A consultation must be booked for one specific animal."
    animal = get_animal(db, animal_id)
    if not animal:
        return "The selected animal does not exist."
    if animal["client_id"] != client_id:
        return "The animal does not belong to this client."
    date = _parse_day(day)
    if not date:
        return "Invalid appointment date."
    if not timetable.is_valid_consult_slot(date.weekday(), time):
        return "That time is not a valid 15-minute consultation slot."
    taken = db.execute(
        "SELECT id FROM appointments WHERE kind='consultation' AND day=? "
        "AND start_time=? AND room=? AND status='booked'",
        (day, time, room)).fetchone()
    if taken:
        return f"Room {room} is already booked at {time} on {day}."
    db.execute(
        "INSERT INTO appointments (client_id, kind, day, start_time, room, "
        "animal_id, reason, status) VALUES (?,?,?,?,?,?,?,'booked')",
        (client_id, "consultation", day, time, room, animal_id, reason))
    db.commit()
    return None


def book_farm_visit(db, client_id, property_id, day, time, duration, reason):
    """Return None on success, else an error message string."""
    if not property_id:
        return "A farm visit must be booked against a property."
    prop = get_property(db, property_id)
    if not prop:
        return "The selected property does not exist."
    if prop["client_id"] != client_id:
        return "The property does not belong to this client."
    date = _parse_day(day)
    if not date:
        return "Invalid appointment date."
    try:
        hours = float(duration)
    except (TypeError, ValueError):
        return "Estimated duration must be a number of hours."
    if hours <= 0:
        return "Estimated duration must be greater than zero hours."
    db.execute(
        "INSERT INTO appointments (client_id, kind, day, start_time, property_id, "
        "duration_hours, reason, status) VALUES (?,?,?,?,?,?,?,'booked')",
        (client_id, "farm_visit", day, time, property_id, hours, reason))
    db.commit()
    return None


def get_appointment(db, appointment_id):
    row = db.execute("SELECT * FROM appointments WHERE id=?",
                     (appointment_id,)).fetchone()
    return _resolve_owner_names(db, row) if row else None


def day_schedule(db, day):
    rows = db.execute(
        "SELECT * FROM appointments WHERE day=? ORDER BY start_time", (day,)).fetchall()
    return [_resolve_owner_names(db, r) for r in rows]


def list_appointments_for_client(db, client_id):
    rows = db.execute(
        "SELECT * FROM appointments WHERE client_id=? ORDER BY day, start_time",
        (client_id,)).fetchall()
    return [_resolve_owner_names(db, r) for r in rows]


def cancel_appointment(db, appointment_id):
    db.execute("UPDATE appointments SET status='cancelled' WHERE id=?",
               (appointment_id,))
    db.commit()


def change_appointment(db, appointment_id, day, time):
    """Move an appointment to a new date/time. Return None or an error string."""
    apt = db.execute("SELECT * FROM appointments WHERE id=?",
                     (appointment_id,)).fetchone()
    if not apt:
        return "Appointment not found."
    if apt["status"] == "cancelled":
        return "A cancelled appointment cannot be moved."
    date = _parse_day(day)
    if not date:
        return "Invalid appointment date."
    if apt["kind"] == "consultation":
        if not timetable.is_valid_consult_slot(date.weekday(), time):
            return "That time is not a valid 15-minute consultation slot."
        taken = db.execute(
            "SELECT id FROM appointments WHERE kind='consultation' AND day=? "
            "AND start_time=? AND room=? AND status='booked' AND id!=?",
            (day, time, apt["room"], appointment_id)).fetchone()
        if taken:
            return f"Room {apt['room']} is already booked at {time} on {day}."
    db.execute("UPDATE appointments SET day=?, start_time=? WHERE id=?",
               (day, time, appointment_id))
    db.commit()
    return None
