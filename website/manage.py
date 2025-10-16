from website import create_app, db
from werkzeug.security import generate_password_hash
from website.models import AUser

def create_admin():
    admin = AUser(
        email="admin@example.com",
        first_name="Admin",
        password=generate_password_hash("adminpassword", method='pbkdf2:sha256'),
        # is_admin=True  # Make sure AUser has this field if needed
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_admin()