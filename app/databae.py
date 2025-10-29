import sqlite3
import os

DB_PATH = os.path.join("data", "apply_me.db")

def init_db():
    """Membuat database & tabel jika belum ada"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_application(company, position, date, status):
    """Menambahkan 1 data lamaran"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO applications (company, position, date, status)
        VALUES (?, ?, ?, ?)
    """, (company, position, date, status))
    conn.commit()
    conn.close()


def get_all_applications():
    """Mengambil semua data lamaran"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM applications ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_application(app_id):
    """Menghapus 1 data berdasarkan ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
