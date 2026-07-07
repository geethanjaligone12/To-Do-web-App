from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT,
        due_time TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    due_date = request.form["date"]
    due_time = request.form["time"]

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks(task,due_date,due_time) VALUES(?,?,?)",
        (task, due_date, due_time)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET completed=1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):

    task = request.form["task"]
    date = request.form["date"]
    time = request.form["time"]

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET task=?, due_date=?, due_time=?
        WHERE id=?
    """, (task, date, time, id))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)