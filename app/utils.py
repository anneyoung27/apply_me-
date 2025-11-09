
from datetime import date
import os
import sys
import subprocess
from PySide6.QtWidgets import QMessageBox


def qdate_to_date(qdate):
    return date(qdate.year(), qdate.month(), qdate.day()) if qdate else None

# === Open file resume and letter ===
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




