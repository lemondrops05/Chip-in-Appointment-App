from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
# from .models import Note
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) #decorator
@login_required #only logged in users can access this route
def home():
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    return render_template("home.html", greeting=greeting, current_user=current_user) #current_user is from flask_login and represents the currently logged in user

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