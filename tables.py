from auth import get_db


def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        enrollment_number TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        marks_scored FLOAT DEFAULT 0.0,
        marks_total FLOAT DEFAULT 100.0,
        attendance_percent FLOAT DEFAULT 0.0,
        ema_history JSON DEFAULT '[50.0]'::json
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id serial PRIMARY KEY,
        username TEXT REFERENCES users(username),
        title TEXT,
        difficulty_weight FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cocurriculars (
        id serial PRIMARY KEY,
        username TEXT REFERENCES users(username),
        event_name TEXT,
        base_type_score FLOAT,
        role_multiplier FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS browser_logs (
        id serial PRIMARY KEY,
        username TEXT REFERENCES users(username),
        domain TEXT,
        minutes_spent FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_dates (
        id serial PRIMARY KEY,
        username TEXT REFERENCES users(username),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
