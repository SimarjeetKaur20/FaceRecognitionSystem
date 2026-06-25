import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/face_recognition.db"
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL UNIQUE,

            registration_date TEXT

        )

        """)

        self.connection.commit()

    def add_user(self, name, registration_date):

        try:

            self.cursor.execute("""

            INSERT INTO users(name, registration_date)

            VALUES(?,?)

            """, (name, registration_date))

            self.connection.commit()

            print("User added successfully.")

        except sqlite3.IntegrityError:

            print("User already exists.")

    def get_all_users(self):

        self.cursor.execute("""

        SELECT * FROM users

        """)

        return self.cursor.fetchall()

    def close(self):

        self.connection.close()