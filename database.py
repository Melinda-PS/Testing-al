import sqlite3

def init_db():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS transcripts (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
    conn.commit()
    conn.close()

def save_transcript(text):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO transcripts (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

def get_all_transcripts():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transcripts')
    rows = c.fetchall()
    conn.close()
    return rows
