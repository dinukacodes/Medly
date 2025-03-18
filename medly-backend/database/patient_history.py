import sqlite3

def get_patient_history(name: str) -> list:
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, condition, treatment FROM patient_history WHERE name = ?", (name,))
    history = [{"date": row[0], "condition": row[1], "treatment": row[2]} for row in cursor.fetchall()]
    conn.close()
    return history