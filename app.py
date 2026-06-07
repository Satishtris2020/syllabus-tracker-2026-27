"""
Syllabus Completion Tracker
Flask backend for GitHub + Railway/Render deployment
"""
import os, json, sqlite3, hashlib
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, abort, session

BASE = Path(__file__).parent
DB   = BASE / "tracker.db"

app = Flask(__name__, static_folder=str(BASE / "static"), static_url_path="")
app.secret_key = os.environ.get("SECRET_KEY", "syllabus-secret-2026")

ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "principal123")
TEACHER_PASS = os.environ.get("TEACHER_PASSWORD", "teacher123")

EXAMS = ["PT1", "PT2", "PT3", "PT4", "PB1", "PB2", "PB3"]

# ── DB ────────────────────────────────────────────────────────────────────────
def db():
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS progress (
            topic_id    TEXT PRIMARY KEY,
            completed   INTEGER DEFAULT 0,
            week_date   TEXT,
            teacher     TEXT,
            updated_at  TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS exam_topics (
            topic_id  TEXT NOT NULL,
            exam      TEXT NOT NULL,
            PRIMARY KEY (topic_id, exam)
        );
        CREATE TABLE IF NOT EXISTS notes (
            topic_id  TEXT PRIMARY KEY,
            note      TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        );
    """)
    con.commit(); con.close()

init_db()

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    role = data.get("role")  # "teacher" or "principal"
    pw   = data.get("password", "")
    if role == "principal" and pw == ADMIN_PASS:
        session["role"] = "principal"; return jsonify({"ok": True, "role": "principal"})
    if role == "teacher" and pw == TEACHER_PASS:
        session["role"] = "teacher"; session["teacher"] = data.get("name","Teacher")
        return jsonify({"ok": True, "role": "teacher"})
    return jsonify({"ok": False, "error": "Wrong password"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear(); return jsonify({"ok": True})

@app.route("/api/whoami")
def whoami():
    return jsonify({"role": session.get("role"), "teacher": session.get("teacher")})

# ── Data ──────────────────────────────────────────────────────────────────────
@app.route("/api/syllabus")
def get_syllabus():
    """Return syllabus structure from embedded JSON."""
    return send_from_directory(str(BASE / "static"), "syllabus_data.json")

@app.route("/api/progress")
def get_progress():
    con = db()
    rows = con.execute("SELECT topic_id, completed, week_date, teacher, updated_at FROM progress").fetchall()
    exams = con.execute("SELECT topic_id, exam FROM exam_topics").fetchall()
    notes = con.execute("SELECT topic_id, note FROM notes").fetchall()
    con.close()
    
    progress = {r["topic_id"]: {
        "completed": bool(r["completed"]),
        "week_date": r["week_date"],
        "teacher":   r["teacher"],
        "updated_at":r["updated_at"],
    } for r in rows}
    
    exam_map = {}
    for e in exams:
        exam_map.setdefault(e["topic_id"], []).append(e["exam"])
    
    note_map = {n["topic_id"]: n["note"] for n in notes}
    
    return jsonify({"progress": progress, "exams": exam_map, "notes": note_map})

@app.route("/api/save", methods=["POST"])
def save_progress():
    if not session.get("role"):
        abort(401)
    data    = request.get_json(force=True)
    updates = data.get("updates", [])   # [{topic_id, completed, week_date, exams, note}]
    teacher = session.get("teacher", "Unknown")
    
    con = db()
    for u in updates:
        tid = u["topic_id"]
        con.execute("""
            INSERT INTO progress (topic_id, completed, week_date, teacher, updated_at)
            VALUES (?,?,?,?, datetime('now'))
            ON CONFLICT(topic_id) DO UPDATE SET
              completed=excluded.completed,
              week_date=excluded.week_date,
              teacher=excluded.teacher,
              updated_at=excluded.updated_at
        """, (tid, 1 if u.get("completed") else 0, u.get("week_date",""), teacher))
        
        # Exams: replace all
        if "exams" in u:
            con.execute("DELETE FROM exam_topics WHERE topic_id=?", (tid,))
            for ex in u["exams"]:
                if ex in EXAMS:
                    con.execute("INSERT OR IGNORE INTO exam_topics VALUES (?,?)", (tid, ex))
        
        # Note
        if "note" in u:
            con.execute("""
                INSERT INTO notes (topic_id, note, updated_at) VALUES (?,?, datetime('now'))
                ON CONFLICT(topic_id) DO UPDATE SET note=excluded.note, updated_at=excluded.updated_at
            """, (tid, u["note"]))
    
    con.commit(); con.close()
    return jsonify({"ok": True, "saved": len(updates)})

# ── Serve SPA ──────────────────────────────────────────────────────────────────
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path and (BASE / "static" / path).exists():
        return send_from_directory(str(BASE / "static"), path)
    return send_from_directory(str(BASE / "static"), "index.html")

if __name__ == "__main__":
    app.run(debug=False, port=int(os.environ.get("PORT", 5000)))
