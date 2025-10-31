import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "apply_me.db")


def get_connection():
    """Helper untuk koneksi database"""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Membuat database & tabel jika belum ada"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS APPLICATION_MASTER (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                COMPANY_NAME TEXT NOT NULL,
                POSITION TEXT NOT NULL,
                LOCATION TEXT,
                DATE_APPLIED DATE NOT NULL,
                SOURCE TEXT,
                STATUS TEXT NOT NULL,
                SALARY_EXPECTATION INTEGER,
                NOTES TEXT,
                RESUME_FILE TEXT,
                COVER_LETTER_FILE TEXT,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def add_application(
    company,
    position,
    date,
    status,
    location=None,
    source=None,
    salary_expectation=None,
    notes=None,
    resume_file=None,
    cover_letter_file=None
):
    """Menambahkan satu data lamaran lengkap ke database"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO APPLICATION_MASTER (
                COMPANY_NAME,
                POSITION,
                LOCATION,
                DATE_APPLIED,
                SOURCE,
                STATUS,
                SALARY_EXPECTATION,
                NOTES,
                RESUME_FILE,
                COVER_LETTER_FILE
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company,
            position,
            location,
            date,
            source,
            status,
            salary_expectation,
            notes,
            resume_file,
            cover_letter_file
        ))
        conn.commit()


def get_all_applications():
    """Mengambil semua data lamaran"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
            SELECT ID, COMPANY_NAME, POSITION, LOCATION, DATE_APPLIED, SOURCE,
                   STATUS, SALARY_EXPECTATION, NOTES,
                   RESUME_FILE, COVER_LETTER_FILE,
                   CREATED_AT, UPDATED_AT
            FROM APPLICATION_MASTER
            ORDER BY ID DESC
        """)
        return c.fetchall()


def get_application_by_id(app_id: int):
    """Mengambil satu data lamaran berdasarkan ID"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM APPLICATION_MASTER WHERE ID = ?", (app_id,))
        return c.fetchone()


def update_application(app_id: int, **fields):
    """
    Mengupdate data lamaran berdasarkan ID.
    Contoh:
        update_application(3, STATUS='Interview', NOTES='Sudah tes HRD')
    """
    if not fields:
        return

    set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values())
    values.append(app_id)

    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f"""
            UPDATE APPLICATION_MASTER
            SET {set_clause},
                UPDATED_AT = ?
            WHERE ID = ?
        """, (*fields.values(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_id))
        conn.commit()


def delete_application(app_id: int):
    """Menghapus 1 data berdasarkan ID"""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM APPLICATION_MASTER WHERE ID = ?", (app_id,))
        conn.commit()
