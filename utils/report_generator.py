import csv
import os
from datetime import datetime


_REPORTS_DIR = "reports"


class ReportGenerator:
    """Generates CSV attendance reports and saves them to the reports/ folder."""

    def __init__(self):
        os.makedirs(_REPORTS_DIR, exist_ok=True)

    def export_to_csv(self, records: list[dict], filename: str = None) -> str:
        """
        Write a list of attendance record dicts to a CSV file.

        Args:
            records:  List of dicts with keys: name, date, time, status
            filename: Optional output filename. Defaults to a timestamped name.

        Returns:
            Absolute path of the written file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attendance_{timestamp}.csv"

        filepath = os.path.join(_REPORTS_DIR, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["name", "date", "time", "status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"Report saved to: {filepath}")
        return os.path.abspath(filepath)
