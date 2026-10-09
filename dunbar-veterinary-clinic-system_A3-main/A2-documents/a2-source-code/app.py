"""Dunbar Veterinary Clinic — appointment system.

A small offline-first Flask + SQLite web application for a mixed-practice
veterinary clinic. This is the A2/A3 project prototype.

Core capabilities:
  - client, animal and property records (CRUD + search)
  - two appointment types: in-clinic consultation and farm visit
  - consultation validation (15-minute slot, timetable, room conflict)
  - farm visit validation (bound to property, duration in hours)
  - change / cancel appointments (cancelled records retained)
  - local SQLite persistence, works without internet
"""

import os

import flask
from flask import Flask, render_template, request, redirect, url_for, flash, abort

from db import get_db, close_db, init_db
import models
import timetable

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["DATABASE"] = os.environ.get(
    "DATABASE_PATH", os.path.join(os.path.dirname(__file__), "data", "clinic.db")
)
app.teardown_appcontext(close_db)


# --------------------------------------------------------------------------
# Index
# --------------------------------------------------------------------------
@app.route("/")
def index():
    db = get_db()
    day = request.args.get("day", "")
    if not day:
        return render_template("index.html")
    rows = models.day_schedule(db, day)
    return render_template("day.html", day=day, rows=rows,
                           booked=[r for r in rows if r["status"] == "booked"],
                           cancelled=[r for r in rows if r["status"] == "cancelled"])


# --------------------------------------------------------------------------
# Clients
# --------------------------------------------------------------------------
@app.route("/clients")
def client_list():
    q = request.args.get("q", "")
    db = get_db()
    rows = models.search_clients(db, q)
    return render_template("client_list.html", rows=rows, q=q)


@app.route("/clients/new", methods=["GET", "POST"])
def client_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        if not name or not phone:
            flash("Client requires a name and at least one contact number.", "error")
            return render_template("client_form.html")
        client_id = models.create_client(get_db(), name, phone,
                                         request.form.get("email", "").strip(),
                                         request.form.get("address", "").strip(),
                                         request.form.get("client_type", "household").strip())
        return redirect(url_for("client_view", client_id=client_id))
    return render_template("client_form.html")


@app.route("/clients/<int:client_id>")
def client_view(client_id):
    db = get_db()
    client = models.get_client(db, client_id)
    if not client:
        abort(404)
    animals = models.list_animals_for_client(db, client_id)
    props = models.list_properties_for_client(db, client_id)
    appointments = models.list_appointments_for_client(db, client_id)
    return render_template("client_view.html", client=client, animals=animals,
                           props=props, appointments=appointments)


@app.route("/clients/<int:client_id>/inactivate", methods=["POST"])
def client_inactivate(client_id):
    models.set_client_active(get_db(), client_id, False)
    flash("Client marked inactive.", "ok")
    return redirect(url_for("client_view", client_id=client_id))


# --------------------------------------------------------------------------
# Animals
# --------------------------------------------------------------------------
@app.route("/animals")
def animal_list():
    q = request.args.get("q", "")
    db = get_db()
    rows = models.search_animals(db, q)
    return render_template("animal_list.html", rows=rows, q=q)


@app.route("/clients/<int:client_id>/animals/new", methods=["GET", "POST"])
def animal_new(client_id):
    db = get_db()
    if not models.get_client(db, client_id):
        abort(404)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        species = request.form.get("species", "").strip()
        if not name or not species:
            flash("Animal requires a name and species.", "error")
            return render_template("animal_form.html", client_id=client_id)
        models.create_animal(db, client_id, name, species,
                             request.form.get("breed", "").strip())
        return redirect(url_for("client_view", client_id=client_id))
    return render_template("animal_form.html", client_id=client_id)


# --------------------------------------------------------------------------
# Properties
# --------------------------------------------------------------------------
@app.route("/clients/<int:client_id>/properties/new", methods=["GET", "POST"])
def property_new(client_id):
    db = get_db()
    if not models.get_client(db, client_id):
        abort(404)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        locality = request.form.get("locality", "").strip()
        if not name or not locality:
            flash("Property requires a name and locality.", "error")
            return render_template("property_form.html", client_id=client_id)
        models.create_property(db, client_id, name, locality,
                               request.form.get("access_notes", "").strip())
        return redirect(url_for("client_view", client_id=client_id))
    return render_template("property_form.html", client_id=client_id)


@app.route("/properties/<int:property_id>/remove", methods=["POST"])
def property_remove(property_id):
    db = get_db()
    prop = models.get_property(db, property_id)
    if not prop:
        abort(404)
    models.remove_property(db, property_id)
    return redirect(url_for("client_view", client_id=prop["client_id"]))


# --------------------------------------------------------------------------
# Appointments
# --------------------------------------------------------------------------
@app.route("/appointments/book", methods=["GET", "POST"])
def appointment_book():
    db = get_db()
    if request.method == "POST":
        kind = request.form.get("kind", "")
        client_id = int(request.form.get("client_id", 0))
        day = request.form.get("day", "")
        time = request.form.get("start_time", "")
        reason = request.form.get("reason", "").strip()
        if kind == "consultation":
            animal_id = int(request.form.get("animal_id", 0))
            room = request.form.get("room", "1")
            error = models.book_consultation(db, client_id, animal_id, day, time, room, reason)
        elif kind == "farm_visit":
            property_id = int(request.form.get("property_id", 0))
            duration = request.form.get("duration_hours", "")
            error = models.book_farm_visit(db, client_id, property_id, day, time, duration, reason)
        else:
            error = "Choose an appointment type."
        if error:
            flash(error, "error")
            return redirect(url_for("appointment_book",
                                    client_id=client_id, kind=kind, day=day))
        return redirect(url_for("index", day=day))
    client_id = request.args.get("client_id", "", type=int)
    kind = request.args.get("kind", "consultation")
    clients = models.all_clients(db)
    animals = models.list_animals_for_client(db, client_id) if client_id else []
    props = models.list_properties_for_client(db, client_id) if client_id else []
    return render_template("appointment_form.html", clients=clients, animals=animals,
                           props=props, client_id=client_id, kind=kind)


@app.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
def appointment_cancel(appointment_id):
    db = get_db()
    apt = models.get_appointment(db, appointment_id)
    if not apt:
        abort(404)
    models.cancel_appointment(db, appointment_id)
    return redirect(url_for("index", day=apt["day"]))


@app.route("/appointments/<int:appointment_id>/change", methods=["GET", "POST"])
def appointment_change(appointment_id):
    db = get_db()
    apt = models.get_appointment(db, appointment_id)
    if not apt:
        abort(404)
    if request.method == "POST":
        day = request.form.get("day", "")
        time = request.form.get("start_time", "")
        error = models.change_appointment(db, appointment_id, day, time)
        if error:
            flash(error, "error")
            return redirect(url_for("appointment_change", appointment_id=appointment_id))
        return redirect(url_for("index", day=day))
    return render_template("change_form.html", apt=apt)


if __name__ == "__main__":
    init_db(app.config["DATABASE"])
    app.run(debug=True)
