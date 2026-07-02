import sqlite3
import os


# Resolve DB path relative to this file so it works
# regardless of the working directory the script is run from.
_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "face_recognition.db"
)


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(_DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def create_tables(self):
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT    NOT NULL UNIQUE,
            registration_date TEXT    NOT NULL,
            label_id          INTEGER NOT NULL DEFAULT -1
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            date         TEXT    NOT NULL,
            time         TEXT    NOT NULL,
            status       TEXT    NOT NULL DEFAULT 'Present',
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE (user_id, date)
        );
        """)
        self.connection.commit()

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def add_user(self, name, registration_date, label_id=-1):
        """Insert a new user. Returns the new row id, or None on duplicate."""
        try:
            self.cursor.execute(
                """
                INSERT INTO users (name, registration_date, label_id)
                VALUES (?, ?, ?)
                """,
                (name, registration_date, label_id),
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def update_user_label(self, name, label_id):
        self.cursor.execute(
            "UPDATE users SET label_id = ? WHERE LOWER(name) = LOWER(?)",
            (label_id, name),
        )
        self.connection.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users ORDER BY id")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_user_by_name(self, name):
        self.cursor.execute(
            "SELECT * FROM users WHERE LOWER(name) = LOWER(?)",
            (name,),
        )
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_user_by_label(self, label_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE label_id = ?",
            (label_id,),
        )
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def user_exists(self, name):
        self.cursor.execute(
            "SELECT 1 FROM users WHERE LOWER(name) = LOWER(?)",
            (name,),
        )
        return self.cursor.fetchone() is not None

    def delete_user(self, name):
        self.cursor.execute(
            "DELETE FROM users WHERE LOWER(name) = LOWER(?)",
            (name,),
        )
        self.connection.commit()
        deleted = self.cursor.rowcount
        if deleted:
            print(f"'{name}' deleted from users table.")
        else:
            print(f"User '{name}' not found.")

    def reset_users_table(self):
        self.cursor.executescript("""
            DELETE FROM attendance;
            DELETE FROM users;
            DELETE FROM sqlite_sequence WHERE name = 'users';
            DELETE FROM sqlite_sequence WHERE name = 'attendance';
        """)
        self.connection.commit()
        print("Users and attendance tables reset successfully.")

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    def mark_attendance(self, name, date, time_str, status="Present"):
        """
        Mark attendance for a user on a given date.
        Silently ignores duplicate (already marked today).
        Returns True if a new record was inserted, False if duplicate.
        """
        user = self.get_user_by_name(name)
        if user is None:
            print(f"Cannot mark attendance — user '{name}' not in DB.")
            return False
        try:
            self.cursor.execute(
                """
                INSERT INTO attendance (user_id, date, time, status)
                VALUES (?, ?, ?, ?)
                """,
                (user["id"], date, time_str, status),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # Already marked today
            return False

    def get_attendance_by_date(self, date):
        self.cursor.execute(
            """
            SELECT u.name, a.date, a.time, a.status
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            WHERE a.date = ?
            ORDER BY a.time
            """,
            (date,),
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def get_attendance_by_user(self, name):
        user = self.get_user_by_name(name)
        if user is None:
            return []
        self.cursor.execute(
            """
            SELECT u.name, a.date, a.time, a.status
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            WHERE a.user_id = ?
            ORDER BY a.date
            """,
            (user["id"],),
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_attendance(self):
        self.cursor.execute(
            """
            SELECT u.name, a.date, a.time, a.status
            FROM attendance a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.date, a.time
            """
        )
        return [dict(row) for row in self.cursor.fetchall()]

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def close(self):
        self.connection.close()