import sqlite3

# Connect to the database file
conn = sqlite3.connect("tournaments.db")
c = conn.cursor()

# Try adding 'game' column
try:
    c.execute("ALTER TABLE registrations ADD COLUMN game TEXT")
    print("Column 'game' added successfully.")
except sqlite3.OperationalError:
    print("Column 'game' already exists.")

# Try adding 'screenshot' column
try:
    c.execute("ALTER TABLE registrations ADD COLUMN screenshot TEXT")
    print("Column 'screenshot' added successfully.")
except sqlite3.OperationalError:
    print("Column 'screenshot' already exists.")

# Commit changes and close
conn.commit()
conn.close()

print("Database schema updated.")
