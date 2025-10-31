import csv
from app.models import Application
from datetime import date

def export_to_csv(session, filepath="applications_export.csv"):
    apps = session.query(Application).all()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Position", "Location", "Date Applied", "Status", "Notes"])
        for app in apps:
            writer.writerow([app.company_name, app.position, app.location, app.date_applied, app.status, app.notes])

def qdate_to_date(qdate):
    return date(qdate.year(), qdate.month(), qdate.day()) if qdate else None
