
import sqlite3

conn = sqlite3.connect("tournaments.db")
c = conn.cursor()

# Create tournaments table
c.execute("""
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT,
    room_id TEXT,
    room_pass TEXT
)
""")

# Create registrations table
c.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    email TEXT,
    pubg_id TEXT,
    tournament_id INTEGER
)
""")

conn.commit()
conn.close()
