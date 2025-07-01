from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # 🔹 Define this FIRST
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔹 Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        pubg_id TEXT,
        game TEXT,
        screenshot TEXT,
        tournament_id INTEGER
    )""")
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    # ✅ No extra indent here
    c.execute("SELECT * FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()

    c.execute("""
        SELECT r.name, r.mobile, r.pubg_id, r.game, t.name as tournament_name, r.screenshot
        FROM registrations r
        JOIN tournaments t ON r.tournament_id = t.id
        ORDER BY r.id DESC
    """)
    registrations = c.fetchall()

    conn.close()
    return render_template("admin.html", tournaments=tournaments, registrations=registrations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()
    print("Fetched tournaments:", tournaments)

    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        pubg_id = request.form['pubg_id']
        game = request.form['game']
        tournament_id = int(request.form['tournament_id'])

        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return render_template("register.html", tournaments=tournaments, error="Invalid screenshot format.")

        c.execute("INSERT INTO registrations (name, mobile, pubg_id, game, screenshot, tournament_id) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, mobile, pubg_id, game, filename, tournament_id))
        conn.commit()
        print(f"[DEBUG] Registered: {name}, {mobile}, {pubg_id}, {game}, Tournament ID: {tournament_id}, Screenshot: {filename}")
        conn.close()
        return render_template("success.html")

    conn.close()
    return render_template("register.html", tournaments=tournaments)

init_db()

if __name__ == '__main__':
    app.run(debug=True)
