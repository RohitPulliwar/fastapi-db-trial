from auth import get_db
from werkzeug.security import check_password_hash, generate_password_hash


def create_user(username, enrollment_number, password):
    conn = get_db()
    password_hash = generate_password_hash(password)

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, enrollment_number, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, username, enrollment_number
            """,
            (username, enrollment_number, password_hash),
        )
        user = cursor.fetchone()
        conn.commit()
        return user
    except Exception:
        conn.rollback()
        return None
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_db()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, enrollment_number, password_hash FROM users WHERE username = %s",
            (username,),
        )
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            return user

        return None
    finally:
        conn.close()


def get_user_data(username):
    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, enrollment_number, marks_scored, marks_total,
                   attendance_percent, ema_history
            FROM users
            WHERE username = %s
            """,
            (username,),
        )
        user = cursor.fetchone()

        if not user:
            return None

        cursor.execute(
            "SELECT title, difficulty_weight FROM skills WHERE username = %s",
            (username,),
        )
        skills = cursor.fetchall()

        cursor.execute(
            """
            SELECT event_name, base_type_score, role_multiplier
            FROM cocurriculars
            WHERE username = %s
            """,
            (username,),
        )
        cocurriculars = cursor.fetchall()

        cursor.execute(
            "SELECT domain, minutes_spent FROM browser_logs WHERE username = %s",
            (username,),
        )
        browser_logs = cursor.fetchall()

        cursor.execute(
            "SELECT timestamp FROM activity_dates WHERE username = %s",
            (username,),
        )
        activity_dates = cursor.fetchall()

        return {
            "id": user[0],
            "username": user[1],
            "enrollment_number": user[2],
            "marks_scored": user[3],
            "marks_total": user[4],
            "attendance_percent": user[5],
            "ema_history": user[6],
            "skills": [
                {"title": skill[0], "difficulty_weight": skill[1]}
                for skill in skills
            ],
            "cocurriculars": [
                {
                    "event_name": item[0],
                    "base_type_score": item[1],
                    "role_multiplier": item[2],
                }
                for item in cocurriculars
            ],
            "browser_logs": [
                {"domain": log[0], "minutes_spent": log[1]}
                for log in browser_logs
            ],
            "activity_dates": [
                {"timestamp": activity[0]}
                for activity in activity_dates
            ],
        }
    finally:
        conn.close()
