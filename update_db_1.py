import sqlite3

conn = sqlite3.connect('tournaments.db')
c = conn.cursor()

# Add 'game' column only if it doesn't already exist
try:
    c.execute("ALTER TABLE tournaments ADD COLUMN game TEXT")
    print("✅ 'game' column added to tournaments table.")
except sqlite3.OperationalError as e:
    print("⚠️ Possibly already exists:", e)

conn.commit()
conn.close()
