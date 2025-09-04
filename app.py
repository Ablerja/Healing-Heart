from flask import Flask, render_template, request
import os, random, sqlite3
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- DB Setup ---
DB_NAME = "healing.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            status TEXT,
            confidence INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    result = None
    if request.method == "POST":
        file = request.files["heartbeat"]
        if file.filename != "":
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Dummy AI Result
            result = random.choice([
                ("Normal 💓", 95),
                ("Minor Irregularity ⚠️", 82),
                ("Consult Doctor 🚑", 70)
            ])

            # Save to DB
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("INSERT INTO results (filename, status, confidence, created_at) VALUES (?,?,?,?)",
                        (file.filename, result[0], result[1], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()

    return render_template("analyze.html", title="Analyze", result=result)

@app.route("/history")
def history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT filename, status, confidence, created_at FROM results ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("history.html", title="History", rows=rows)
@app.route('/tips')
def tips():
    return render_template('tips.html')
@app.route('/future')
def future():
    return render_template('future.html')



if __name__ == "__main__":
    app.run(debug=True)
