# database.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            type TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_transcript(text, transcript_type="speech"):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO transcripts (text, type, timestamp) VALUES (?, ?, ?)',
        (text, transcript_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_all_transcripts():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_transcripts_by_type(transcript_type):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts WHERE type = ? ORDER BY timestamp DESC', (transcript_type,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_transcript(transcript_id):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute('DELETE FROM transcripts WHERE id = ?', (transcript_id,))
    conn.commit()
    conn.close()
