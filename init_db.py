from website import create_app, db
from website.models import AUser, Service
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()  # Create all tables

    # Check if admin already exists
    if not AUser.query.filter_by(email="udei@uwindsor.ca").first():
        admin = AUser(
            email="udei@uwindsor.ca",
            first_name="Admin",
            password=generate_password_hash("apassword", method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
    
    services_to_add = [
        {
            "name": "Acrylic Manicure",
            "description": "Acrylic nails with a variety of colors.",
            "duration": 60,
            "price": 50.00
        },
        {
            "name": "Gel Manicure",
            "description": "Gel nails with long-lasting shine.",
            "duration": 60,
            "price": 60.00
        },
        {
            "name": "Nail Art",
            "description": "Creative nail art designs.",
            "duration": 90,
            "price": 70.00
        }
    ]

    for s in services_to_add:
        if not Service.query.filter_by(name=s["name"]).first():
            service = Service(
                name=s["name"],
                description=s["description"],
                duration=s["duration"],
                price=s["price"]
            )
            db.session.add(service)
            print(f"Added service: {s['name']}")
        else:
            print(f"Service already exists: {s['name']}")
    db.session.commit()