
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT,
        room_id TEXT,
        room_pass TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        email TEXT,
        pubg_id TEXT,
        tournament_id INTEGER
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        room_id = request.form['room_id']
        room_pass = request.form['room_pass']
        c.execute("INSERT INTO tournaments (name, date, time, room_id, room_pass) VALUES (?, ?, ?, ?, ?)",
                  (name, date, time, room_id, room_pass))
        conn.commit()
    c.execute("SELECT * FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()
    conn.close()
    return render_template("admin.html", tournaments=tournaments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        pubg_id = request.form['pubg_id']
        tournament_id = request.form['tournament_id']
        c.execute("INSERT INTO registrations (name, mobile, email, pubg_id, tournament_id) VALUES (?, ?, ?, ?, ?)",
                  (name, mobile, email, pubg_id, tournament_id))
        conn.commit()
        conn.close()
        return render_template("success.html")
    conn.close()
    return render_template("register.html", tournaments=tournaments)

init_db()  # ensure DB is created even on Render

if __name__ == '__main__':
    app.run(debug=True)

