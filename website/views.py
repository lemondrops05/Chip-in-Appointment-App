from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .models import Appointment, Service, AUser
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) #decorator
@login_required #only logged in users can access this route
def home():
    services = Service.query.all()
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    return render_template("home.html", greeting=greeting, current_user=current_user, services=services) #current_user is from flask_login and represents the currently logged in user

# @views.route('/delete-note', methods=['POST']) #decorator
# @login_required
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id: #only the user who created the note can delete it
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})
@views.route('/a_book/<int:service_id>')
def a_book(service_id):
    service = Service.query.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('views.home'))
    return render_template("a_book.html")

@views.route('/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    date_str = request.form.get('appointment_date')
    time_str = request.form.get('appointment_time')
    # Combine date and time into a datetime object
    start_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
    end_time = start_time  # You can add duration logic if needed

    # Find the service (assuming Acrylic Manicure has id=1, adjust as needed)
    service = Service.query.filter_by(name="Acrylic Manicure").first()
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for('views.a_book'))

    appointment = Appointment(
        user_id=current_user.id,
        service_id=service.id,
        start_time=start_time,
        end_time=start_time,  # Or calculate end_time based on duration
        status='Confirmed'
    )
    db.session.add(appointment)
    db.session.commit()
    flash("Appointment booked!", "success")
    return redirect(url_for('views.home'))

@views.route('/my_appointments')
@login_required
def my_appointments():
    now = datetime.now()
    upcoming = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.start_time >= now
    ).order_by(Appointment.start_time.asc()).all()
    past = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.start_time < now
    ).order_by(Appointment.start_time.desc()).all()
    return render_template("user_apps.html", upcoming=upcoming, past=past)

@views.route('/admin/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    if not getattr(current_user, 'is_admin', False):
        flash('Admins only!', 'error')
        return redirect(url_for('auth.admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        duration = request.form.get('duration')
        price = request.form.get('price')
        if name:
            service = Service(
                name=name,
                description=description,
                duration=int(duration) if duration else 240,
                price=float(price) if price else 0.0
            )
            db.session.add(service)
            db.session.commit()
            flash('Service added!', 'success')
        else:
            flash('Service name is required.', 'error')

    # Always reload the dashboard with the updated list
    services = Service.query.all()
    return render_template('admin_dash.html', services=services)

@views.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment and appointment.user_id == current_user.id:
        db.session.delete(appointment)
        db.session.commit()
        return '', 204  # Success, no content
    return '', 403  # Forbidden