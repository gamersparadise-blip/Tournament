# create_sample.py
import sqlite3

conn = sqlite3.connect('tournaments.db')
c = conn.cursor()
c.execute("INSERT INTO tournaments (name, date, time, room_id, room_pass) VALUES (?, ?, ?, ?, ?)",
          ("Test Match", "2025-07-01", "18:00", "Room123", "pass123"))
conn.commit()
conn.close()

print("Test tournament inserted successfully.")
