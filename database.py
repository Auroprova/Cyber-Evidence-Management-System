import sqlite3

def init_db():

    conn = sqlite3.connect("cases.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint TEXT,
        category TEXT,
        severity TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER,
        file_name TEXT,
        sha256_hash TEXT
    )
    """)

    conn.commit()
    conn.close()

print("Database Ready")