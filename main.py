"""
Face Recognition Attendance System
===================================
Run this file from the project root:

    python main.py

Menu options:
    1 — Register new user  (capture faces + add to DB)
    2 — Train model        (build/rebuild LBPH model)
    3 — Start recognition  (live webcam + attendance marking)
    4 — View today's attendance
    5 — View all attendance
    6 — Export today's attendance to CSV
    7 — Export all attendance to CSV
    8 — Delete a user
    9 — List all registered users
    0 — Exit
"""

import os
import sys


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_menu():
    print("\n" + "=" * 45)
    print("   Face Recognition Attendance System")
    print("=" * 45)
    print("  1. Register New User")
    print("  2. Train Model")
    print("  3. Start Face Recognition (mark attendance)")
    print("  4. View Today's Attendance")
    print("  5. View All Attendance")
    print("  6. Export Today's Attendance to CSV")
    print("  7. Export All Attendance to CSV")
    print("  8. Delete a User")
    print("  9. List All Registered Users")
    print("  0. Exit")
    print("=" * 45)


def main():
    # Lazy imports — only load heavy libs when actually needed
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            from services.user_registration import UserRegistration
            reg = UserRegistration()
            reg.register_user()

        elif choice == "2":
            from services.face_trainer import FaceTrainer
            trainer = FaceTrainer()
            label_map = trainer.train_model()
            if label_map:
                print("\nLabel map:")
                for label, name in label_map.items():
                    print(f"  {label}: {name}")

        elif choice == "3":
            from services.face_recognizer import FaceRecognizer
            try:
                recognizer = FaceRecognizer()
                recognizer.recognize_faces()
            except FileNotFoundError as e:
                print(f"\nError: {e}")

        elif choice == "4":
            from services.attendance_service import AttendanceService
            svc = AttendanceService()
            svc.print_today_attendance()
            svc.close()

        elif choice == "5":
            from services.attendance_service import AttendanceService
            svc = AttendanceService()
            svc.print_all_attendance()
            svc.close()

        elif choice == "6":
            from services.attendance_service import AttendanceService
            svc = AttendanceService()
            path = svc.export_today_to_csv()
            svc.close()

        elif choice == "7":
            from services.attendance_service import AttendanceService
            svc = AttendanceService()
            path = svc.export_all_to_csv()
            svc.close()

        elif choice == "8":
            name = input("Enter the user name to delete: ").strip()
            if name:
                confirm = input(
                    f"Are you sure you want to delete '{name}' and their dataset? (y/n): "
                ).strip().lower()
                if confirm == "y":
                    from services.user_registration import UserRegistration
                    reg = UserRegistration()
                    reg.delete_user(name)
            else:
                print("Name cannot be empty.")

        elif choice == "9":
            from database.database import Database
            db = Database()
            users = db.get_all_users()
            db.close()
            print("\nRegistered Users")
            print("-" * 40)
            if not users:
                print("No users registered yet.")
            else:
                print(f"  {'ID':<5} {'Name':<20} {'Registered':<15} {'Label'}")
                print("  " + "-" * 50)
                for u in users:
                    print(
                        f"  {u['id']:<5} {u['name']:<20} "
                        f"{u['registration_date']:<15} {u['label_id']}"
                    )
            print()

        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
