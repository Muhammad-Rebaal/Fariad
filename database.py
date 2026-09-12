import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'fariad.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    """Initialize the database with the schema if it doesn't exist."""
    is_new = not os.path.exists(DB_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        if is_new:
            print("Initializing database...")
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
        else:
            print("Database already initialized.")

def get_or_create_user(name: str, email: str, district: str, postal_code: str, street: str) -> int:
    """Gets an existing user by email, or creates a new one. Returns the user ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Check if user exists by email
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        if row:
            # Update existing user's details just in case they changed
            cursor.execute("""
                UPDATE users 
                SET name = ?, district = ?, postal_code = ?, street = ?
                WHERE id = ?
            """, (name, district, postal_code, street, row[0]))
            conn.commit()
            return row[0]
        else:
            # Insert new user
            cursor.execute("""
                INSERT INTO users (name, email, district, postal_code, street)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, district, postal_code, street))
            conn.commit()
            return cursor.lastrowid

def create_complaint(user_id: int, complaint_text: str, complaint_type: str = "General", department: str = "Unknown") -> int:
    """Creates a new complaint record."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO complaints (user_id, complaint_type, complaint, complaint_department, tracking_no, filed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, complaint_type, complaint_text, department, "PENDING", 0))
        conn.commit()
        return cursor.lastrowid
