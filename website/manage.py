from website import db
from website.models import User, SUser, AUser, Note

def clear_tables():
    db.session.query(Note).delete()
    db.session.query(User).delete()
    db.session.query(SUser).delete()
    db.session.query(AUser).delete()
    db.session.commit()
    print("All tables cleared.")

if __name__ == "__main__":
    clear_tables()