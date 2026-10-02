"""Test suite for the Dunbar clinic appointment system.

Covers the core domain rules, especially the clinic's two kinds of
appointment (in-clinic consultation and farm visit), validation, persistence
and change/cancel behaviour.
"""

import sqlite3
import tempfile
import os

import pytest

import db as db_module
import models
import timetable
from app import app


def make_world(db):
    """Seed a minimal clinic world: a client, an animal and a property."""
    cid = models.create_client(db, "Mrs Prosser", "0417 552 118", client_type="household")
    aid = models.create_animal(db, cid, "Biscuit", "cat", "DSH")
    pid = models.create_property(db, cid, "Kalinga Downs", "Coulson", "Gate code 4417")
    return cid, aid, pid


# --------------------------------------------------------------------------
# US-01 Clients
# --------------------------------------------------------------------------
def test_create_and_search_client(app):
    with app.app_context():
        db = db_module.get_db()
        models.create_client(db, "Mrs Prosser", "0417 552 118")
        models.create_client(db, "Mrs Kelso", "0413 660 288")
        rows = models.search_clients(db, "prosser")
        assert len(rows) == 1
        assert rows[0]["name"] == "Mrs Prosser"
        # every match returned
        models.create_client(db, "Smith A", "0400 000 001")
        models.create_client(db, "Smith B", "0400 000 002")
        assert len(models.search_clients(db, "smith")) == 2


# --------------------------------------------------------------------------
# US-02 Animals
# --------------------------------------------------------------------------
def test_add_list_and_search_animal(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, _ = make_world(db)
        models.create_animal(db, cid, "Ruby", "cat")
        models.create_animal(db, cid, "Sooty", "cat")
        # make_world already added Biscuit, so the client has three animals
        assert len(models.list_animals_for_client(db, cid)) == 3
        # search by animal name across all clients
        cid2 = models.create_client(db, "Other", "0400 000 003")
        models.create_animal(db, cid2, "Ruby", "dog")
        assert len(models.search_animals(db, "Ruby")) == 2


def test_animal_requires_existing_client(app):
    with app.app_context():
        db = db_module.get_db()
        # FK constraint: cannot attach animal to a client that does not exist
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(
                "INSERT INTO animals (client_id, name, species) VALUES (999999, 'X', 'cat')")
            db.commit()


# --------------------------------------------------------------------------
# US-03 Properties
# --------------------------------------------------------------------------
def test_property_create_list_remove(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, _ = make_world(db)
        pid2 = models.create_property(db, cid, "Stony Creek", "Bunjurgen",
                                      "3 gates; last one has a chain, no code")
        assert len(models.list_properties_for_client(db, cid)) == 2
        models.remove_property(db, pid2)
        assert len(models.list_properties_for_client(db, cid)) == 1


def test_client_may_have_neither_animal_nor_property(app):
    with app.app_context():
        db = db_module.get_db()
        cid = models.create_client(db, "Bare Farm", "0400 000 004")
        assert models.list_animals_for_client(db, cid) == []
        assert models.list_properties_for_client(db, cid) == []


# --------------------------------------------------------------------------
# US-04 Persistence
# --------------------------------------------------------------------------
def test_data_persists_across_restart():
    """Records survive when the database file is re-opened."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "persist.db")
        db_module.init_db(path)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cid = models.create_client(conn, "Kelso", "0413 660 288")
        models.create_animal(conn, cid, "Ruby", "cat")
        conn.close()

        # simulate an application restart: reopen the same file
        conn2 = sqlite3.connect(path)
        conn2.row_factory = sqlite3.Row
        clients = conn2.execute("SELECT * FROM clients").fetchall()
        animals = conn2.execute("SELECT * FROM animals").fetchall()
        conn2.close()
        assert len(clients) == 1 and clients[0]["name"] == "Kelso"
        assert len(animals) == 1 and animals[0]["name"] == "Ruby"


# --------------------------------------------------------------------------
# US-05 In-clinic consultation
# --------------------------------------------------------------------------
def test_book_valid_consultation(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        err = models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "F3 vacc")
        assert err is None
        schedule = models.day_schedule(db, "2026-09-07")
        assert len(schedule) == 1
        assert schedule[0]["status"] == "booked"
        assert schedule[0]["kind"] == "consultation"


def test_consultation_without_animal_invalid(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, _ = make_world(db)
        err = models.book_consultation(db, cid, 0, "2026-09-07", "08:30", "1", "check")
        assert "animal" in err.lower()


def test_consultation_time_off_timetable_invalid(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        # 10:20 is not on the 15-minute grid
        assert models.book_consultation(db, cid, aid, "2026-09-07", "10:20", "1", "") is not None
        # Sunday is closed
        assert models.book_consultation(db, cid, aid, "2026-09-06", "09:00", "1", "") is not None
        # after 10:15 on a Tuesday is not a consult slot
        assert models.book_consultation(db, cid, aid, "2026-09-08", "14:00", "1", "") is not None


def test_consultation_room_conflict(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        assert models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "") is None
        # same room, same slot -> conflict
        err = models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "")
        assert err is not None
        # other room, same slot -> allowed
        assert models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "2", "") is None


def test_timetable_slot_times():
    # Monday has 15-min slots through to 17:15, excluding held 11:15/11:30
    times = timetable.slot_times(0)
    assert "08:30" in times and "17:15" in times
    assert "11:15" not in times and "11:30" not in times
    # Sunday has no slots
    assert timetable.slot_times(6) == []


# --------------------------------------------------------------------------
# US-06 Farm visit
# --------------------------------------------------------------------------
def test_book_valid_farm_visit(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, pid = make_world(db)
        err = models.book_farm_visit(db, cid, pid, "2026-09-08", "11:15", "3.0", "Preg test, 120 head")
        assert err is None
        schedule = models.day_schedule(db, "2026-09-08")
        assert len(schedule) == 1
        assert schedule[0]["kind"] == "farm_visit"
        assert schedule[0]["duration_hours"] == 3.0


def test_farm_visit_without_property_invalid(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, _ = make_world(db)
        err = models.book_farm_visit(db, cid, 0, "2026-09-08", "11:15", "3.0", "")
        assert "property" in err.lower()


def test_farm_visit_duration_must_be_positive(app):
    with app.app_context():
        db = db_module.get_db()
        cid, _, pid = make_world(db)
        assert models.book_farm_visit(db, cid, pid, "2026-09-08", "11:15", "0", "") is not None
        assert models.book_farm_visit(db, cid, pid, "2026-09-08", "11:15", "-2", "") is not None
        # free-form hours not constrained to 15-minute slots is accepted
        assert models.book_farm_visit(db, cid, pid, "2026-09-08", "11:15", "2.5", "") is None


def test_farm_visit_requires_a_real_property(app):
    """A farm visit must bind to a valid property that belongs to the client."""
    with app.app_context():
        db = db_module.get_db()
        cid, _, pid = make_world(db)
        # a property id that does not exist is rejected
        err = models.book_farm_visit(db, cid, 999999, "2026-09-08", "11:15", "3.0", "")
        assert err is not None
        # a property belonging to another client is rejected (wrong attachment)
        cid2 = models.create_client(db, "Other Farm Co", "0400 000 003")
        pid2 = models.create_property(db, cid2, "Other Farm", "Milford", "")
        err2 = models.book_farm_visit(db, cid, pid2, "2026-09-08", "11:15", "3.0", "")
        assert err2 is not None


# --------------------------------------------------------------------------
# US-07 Change and cancel
# --------------------------------------------------------------------------
def test_change_appointment_does_not_affect_others(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        assert models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "") is None
        assert models.book_consultation(db, cid, aid, "2026-09-07", "09:00", "1", "") is None
        a1 = models.day_schedule(db, "2026-09-07")[0]["id"]
        a2 = models.day_schedule(db, "2026-09-07")[1]["id"]
        err = models.change_appointment(db, a1, "2026-09-09", "10:00")
        assert err is None
        sched = models.day_schedule(db, "2026-09-07")
        # appointment 2 unchanged
        assert [a["id"] for a in sched] == [a2]
        assert models.get_appointment(db, a1)["day"] == "2026-09-09"


def test_cancel_retains_record_and_is_distinguishable(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        assert models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "") is None
        apt_id = models.day_schedule(db, "2026-09-07")[0]["id"]
        models.cancel_appointment(db, apt_id)
        schedule = models.day_schedule(db, "2026-09-07")
        # cancelled appointment remains visible
        assert len(schedule) == 1
        assert schedule[0]["status"] == "cancelled"
        # cancelled cannot be re-booked into the same room/slot
        assert models.book_consultation(db, cid, aid, "2026-09-07", "08:30", "1", "") is None


def test_new_appointment_starts_booked(app):
    with app.app_context():
        db = db_module.get_db()
        cid, aid, _ = make_world(db)
        assert models.book_consultation(db, cid, aid, "2026-09-07", "09:30", "1", "") is None
        assert models.day_schedule(db, "2026-09-07")[0]["status"] == "booked"
