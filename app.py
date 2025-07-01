from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        game TEXT,
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect('/register')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        game = request.form['game']
        date = request.form['date']
        time = request.form['time']
        room_id = request.form['room_id']
        room_pass = request.form['room_pass']
        c.execute("INSERT INTO tournaments (name, game, date, time, room_id, room_pass) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, game, date, time, room_id, room_pass))
        conn.commit()

    c.execute("SELECT id, name FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()

    selected_id = request.args.get('filter_tournament')
    if selected_id:
        c.execute("""
            SELECT r.name, r.mobile, r.pubg_id, r.game, t.name, r.screenshot
            FROM registrations r
            JOIN tournaments t ON r.tournament_id = t.id
            WHERE t.id = ?
            ORDER BY r.id DESC
        """, (selected_id,))
    else:
        c.execute("""
            SELECT r.name, r.mobile, r.pubg_id, r.game, t.name, r.screenshot
            FROM registrations r
            JOIN tournaments t ON r.tournament_id = t.id
            ORDER BY r.id DESC
        """)

    registrations = c.fetchall()
    conn.close()

    return render_template("admin.html", tournaments=tournaments, registrations=registrations, selected_id=selected_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM tournaments ORDER BY id DESC")
    tournaments = c.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        pubg_id = request.form['pubg_id']
        tournament_id = int(request.form['tournament_id'])

        # Fetch game for the selected tournament
        c.execute("SELECT game FROM tournaments WHERE id = ?", (tournament_id,))
        result = c.fetchone()
        game = result[0] if result else "Unknown"

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
        conn.close()
        return render_template("success.html")

    conn.close()
    return render_template("register.html", tournaments=tournaments)

@app.route('/get_game_for_tournament/<int:tournament_id>')
def get_game_for_tournament(tournament_id):
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()
    c.execute("SELECT game FROM tournaments WHERE id = ?", (tournament_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"game": result[0]})
    else:
        return jsonify({"game": ""})

init_db()

if __name__ == '__main__':
    app.run(debug=True)
