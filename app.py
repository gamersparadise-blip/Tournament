from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        tournament_id INTEGER,
        game TEXT,
        screenshot TEXT
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
        game = request.form['game']

        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
        else:
            return render_template("register.html", tournaments=tournaments, error="Invalid screenshot format.")

        c.execute("INSERT INTO registrations (name, mobile, email, pubg_id, tournament_id, game, screenshot) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, mobile, email, pubg_id, tournament_id, game, filename))
        conn.commit()
        conn.close()
        return render_template("success.html")

    conn.close()
    return render_template("register.html", tournaments=tournaments)


# Initialize database even on Render
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

