import csv
from app.models import Application
from datetime import date
import os
import sys
import subprocess
from PySide6.QtWidgets import QMessageBox

def export_to_csv(session, filepath="applications_export.csv"):
    apps = session.query(Application).all()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Position", "Location", "Date Applied", "Status", "Notes"])
        for app in apps:
            writer.writerow([app.company_name, app.position, app.location, app.date_applied, app.status, app.notes])

def qdate_to_date(qdate):
    return date(qdate.year(), qdate.month(), qdate.day()) if qdate else None

def open_file(path):
    if not path:
        QMessageBox.warning(None, "File Not Found", "No file attached for this application.")
        return

    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to open file:\n{str(e)}")


