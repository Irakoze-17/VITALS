from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS happiness (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        happiness_score INTEGER,
        alert TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

students = {
    "student1": "1234"
}

staff_members = {
    "staff1": "admin123"
}

@app.route("/")
def home():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if role == "student":
        if username in students and students[username] == password:
            return redirect(url_for("student_dashboard"))

    if role == "staff":
        if username in staff_members and staff_members[username] == password:
            return redirect(url_for("staff_dashboard"))

    return "Invalid login details"
@app.route("/logout")
def logout():
    return redirect(url_for("home"))
@app.route("/student_dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")
@app.route("/submit_happiness", methods=["POST"])
def submit_happiness():

    name = request.form["name"]
    score = int(request.form["score"])

    alert = "Normal"

    if score <= 30:
        alert = "⚠ Low Happiness"

    elif score >= 85:
        alert = "⚠ Unusually High Happiness"

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO happiness (student_name, happiness_score, alert) VALUES (?, ?, ?)",
        (name, score, alert)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("student_dashboard"))
@app.route("/staff_dashboard")
def staff_dashboard():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM happiness")
    records = cursor.fetchall()

    conn.close()

    return render_template("staff_dashboard.html", records=records)
if __name__ == "__main__":
    app.run(debug=True)
