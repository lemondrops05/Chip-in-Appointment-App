import sqlite3

def setup_database():
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect("chipin.db")
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    # Create Admins table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    # Create Services table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
            ("user1", "password1"),
            ("user2", "password2")
        ])

    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admins (admin_id, password) VALUES (?, ?)",
            ("admin1", "adminpass1")
        )
    
    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO services (name) VALUES (?)", [
            ("Gel-x",),
            ("Acrylic",),
            ("BIAB",)
        ])

    # Commit changes and close connection
    conn.commit()
    conn.close()

def add_user(username, password):
    try:
        with sqlite3.connect("chipin.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")

