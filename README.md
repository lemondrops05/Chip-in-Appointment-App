# Chip-in — Appointment App

Short description
- Small Flask app for booking nail appointments. Users can view services and book slots. SQLite used for persistence.

Features
- User authentication (Flask-Login)
- Separate admin model (AUser) and user model (User)
- Services listing with "Book Now"
- Book appointments, list upcoming & past appointments
- Delete upcoming appointments (client-side JS + server route)

Requirements
- Python 3.10+ (3.13 tested)
- pip
- virtualenv (recommended)
- Dependencies listed in `requirements.txt` (Flask, Flask-Login, Flask-SQLAlchemy, Werkzeug, ...)

Quick setup (macOS)
1. Clone repo (if not already)
   - git clone <repo-url>

2. Create venv and install
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Initialize database + create default admin and sample services
   - `init_db.py` runs db.create_all() and inserts seed data.
   ```bash
   PYTHONPATH=. python3 init_db.py
   ```
   - Default admin in the seed script:
     - Email: `admin@example.com`
     - Password: `adminpassword`
   - If you changed the admin email in `init_db.py`, use that email.

Run the app
```bash
python3 main.py
```
Open: http://127.0.0.1:5000

Key files & purpose
- main.py — app entry
- website/__init__.py — create_app(), DB and LoginManager setup, user_loader
- website/models.py — DB models: User, AUser, Appointment, Service (check file for current classes)
- website/views.py — main routes (home, booking, my_appointments, admin routes)
- website/auth.py — login / signup / admin login
- website/manage.py / init_db.py — helper scripts to create admin / seed services
- website/templates/ — Jinja templates (home.html, a_book.html, admin_dash.html, user_apps.html, base.html, etc.)
- website/static/index.js — JS functions (deleteAppointment, deleteNote)

Admin usage
- Visit `/admin/login` to sign in as admin.
- After login, `/admin/add_service` (admin dashboard) lets you add services.
- Admin dashboard reloads and shows updated services; it should not redirect to login if you are an authenticated admin.

Booking flow
- Home lists services (`services` passed from views.py).
- "Book Now" links to `/a_book/<service_id>` (route must accept service_id).
- Booking form posts to `/book_appointment` which creates an Appointment row.

Delete appointment (user)
- JS: `deleteAppointment(appointmentId)` sends POST to `/delete_appointment/<id>`.
- Server route deletes appointment if owned by current user and returns success; page reloads to reflect change.

Common issues & fixes
- "no such column" errors: you changed models after DB creation. Delete DB and re-run init:
  ```bash
  rm website/database.db
  PYTHONPATH=. python3 init_db.py
  ```
  Or use Flask-Migrate for production migrations.

- Flask-Login with multiple user tables:
  - Models should implement `get_id()` to return a composite id like `admin-1` or `user-2`.
  - In `website/__init__.py` implement user_loader that splits the composite id and queries the correct model.

  Example load_user:
  ```python
  @login_manager.user_loader
  def load_user(composite_id):
      try:
          user_type, user_id = composite_id.split('-')
          if user_type == 'user': return User.query.get(int(user_id))
          if user_type == 'admin': return AUser.query.get(int(user_id))
      except Exception:
          return None
  ```

- Jinja errors ("undefined variable" / "unexpected '}'"): check templates for missing loop or braces; ensure `services` is passed from the view to `home.html`.

Notes
- Secrets: replace the hardcoded `SECRET_KEY` in `website/__init__.py` with a secure value for production.
- If you want help modifying specific files (models, views, templates) paste them and request the exact change.

Contact / next steps
- Tell me which environment you run (`python3 main.py` output) or paste the current `models.py` and `views.py` if you want me to generate exact code snippets (models, routes, or templates) to finish admin/user flows.
