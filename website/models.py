from . import db
from flask_login import UserMixin

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #relationship with user table one-to-many. that is one user to many notes

class User(db.Model, UserMixin): #usermixin only for user to inherit
    __tablename__ = 'users'  # <-- Add this line
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note') #relationship with note table one-to-many. that is one user to many notes

    @property
    def user_type(self):
        return "user"
    
    def get_id(self):
        return f"{self.user_type}-{self.id}"  # <-- Add this method


# class SUser(db.Model, UserMixin): #usermixin only for user to inherit
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     # notes = db.relationship('Note') #relationship with note table one-to-many. that is one user to many notes

class AUser(db.Model, UserMixin): #usermixin only for user to inherit
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=True)

    @property
    def user_type(self):
        return "admin"
    
    def get_id(self):
        return f"{self.user_type}-{self.id}"  # <-- Add this method


# 💅 SERVICES
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    duration = db.Column(db.Integer, default=240)  # in minutes (4 hours)
    price = db.Column(db.Float)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy=True)

# 📅 APPOINTMENTS
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # <-- Change 'User.id' to 'users.id'
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    calendar_event_id = db.Column(db.String(200))  # Google Calendar Event ID
    status = db.Column(db.String(50), default='Confirmed')