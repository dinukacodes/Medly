import sqlite3
import json

def save_patient_data(patient_data: dict, session_id: str):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    patient_data_json = json.dumps(patient_data)
    cursor.execute("INSERT OR REPLACE INTO sessions (session_id, patient_data, reasoning_steps, diagnosis) VALUES (?, ?, ?, ?)",
                   (session_id, patient_data_json, json.dumps([]), json.dumps({})))
    conn.commit()
    conn.close()

def save_state_to_db(session_id: str, state: dict):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    reasoning_steps = json.dumps(state["reasoning_steps"])
    diagnosis = json.dumps(state.get("diagnosis", {}))
    cursor.execute("UPDATE sessions SET reasoning_steps = ?, diagnosis = ? WHERE session_id = ?",
                   (reasoning_steps, diagnosis, session_id))
    conn.commit()
    conn.close()

def get_session_state(session_id: str) -> dict:
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT patient_data, reasoning_steps, diagnosis FROM sessions WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        patient_data = json.loads(result[0])
        reasoning_steps = json.loads(result[1])
        diagnosis = json.loads(result[2])
        return {
            "patient_data": patient_data,
            "reasoning_steps": reasoning_steps,
            "diagnosis": diagnosis
        }
    return {}