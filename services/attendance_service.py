from datetime import datetime

from database.database import Database
from utils.report_generator import ReportGenerator


class AttendanceService:
    """
    High-level attendance operations: view, export, and summary.
    """

    def __init__(self):
        self.db = Database()
        self.report_generator = ReportGenerator()

    # ------------------------------------------------------------------
    # View helpers
    # ------------------------------------------------------------------

    def get_today_attendance(self):
        today = datetime.now().strftime("%d-%m-%Y")
        return self.db.get_attendance_by_date(today)

    def get_attendance_for_date(self, date: str):
        """date format: DD-MM-YYYY"""
        return self.db.get_attendance_by_date(date)

    def get_attendance_for_user(self, name: str):
        return self.db.get_attendance_by_user(name)

    def get_all_attendance(self):
        return self.db.get_all_attendance()

    # ------------------------------------------------------------------
    # Display helpers (terminal)
    # ------------------------------------------------------------------

    def print_today_attendance(self):
        today = datetime.now().strftime("%d-%m-%Y")
        records = self.get_today_attendance()
        print(f"\nAttendance for {today}")
        print("-" * 40)
        if not records:
            print("No attendance records for today.")
        else:
            for r in records:
                print(f"  {r['name']:<20} {r['time']}  [{r['status']}]")
        print()

    def print_all_attendance(self):
        records = self.get_all_attendance()
        print("\nAll Attendance Records")
        print("-" * 55)
        if not records:
            print("No records found.")
        else:
            for r in records:
                print(
                    f"  {r['name']:<20} {r['date']}  {r['time']}  [{r['status']}]"
                )
        print()

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_today_to_csv(self) -> str:
        """Export today's attendance to a CSV file. Returns the file path."""
        records = self.get_today_attendance()
        today = datetime.now().strftime("%d-%m-%Y")
        path = self.report_generator.export_to_csv(records, filename=f"attendance_{today}.csv")
        return path

    def export_all_to_csv(self) -> str:
        """Export all attendance records to a CSV file. Returns the file path."""
        records = self.get_all_attendance()
        path = self.report_generator.export_to_csv(records, filename="attendance_full.csv")
        return path

    def export_user_to_csv(self, name: str) -> str:
        """Export a single user's attendance to CSV. Returns the file path."""
        records = self.get_attendance_for_user(name)
        safe_name = name.replace(" ", "_").lower()
        path = self.report_generator.export_to_csv(
            records, filename=f"attendance_{safe_name}.csv"
        )
        return path

    # ------------------------------------------------------------------

    def close(self):
        self.db.close()
