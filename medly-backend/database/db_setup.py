import sqlite3

def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            patient_data TEXT,
            reasoning_steps TEXT,
            diagnosis TEXT
        )
    """)
    
    # Create patient_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            condition TEXT,
            treatment TEXT
        )
    """)
    
    # Create evidence table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            file_id TEXT PRIMARY KEY,
            text TEXT
        )
    """)
    
    # Insert mock data
    cursor.execute("INSERT OR IGNORE INTO patient_history (name, date, condition, treatment) VALUES (?, ?, ?, ?)",
                   ("Jane Doe", "2022-01-15", "Flu", "Oseltamivir"))
    cursor.execute("INSERT OR IGNORE INTO patient_history (name, date, condition, treatment) VALUES (?, ?, ?, ?)",
                   ("John Smith", "2023-03-10", "Hypertension", "Lisinopril"))
    
    conn.commit()
    conn.close()