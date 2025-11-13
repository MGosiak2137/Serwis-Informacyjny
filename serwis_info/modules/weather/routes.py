from flask import render_template, jsonify, request
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    default_city TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    city TEXT
)
""")
conn.commit()

def get_user_id(username: str) -> int:
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row:
        return row[0]
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return c.lastrowid

def register_routes(bp):
    @bp.route('/')
    @bp.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')

    @bp.route('/api/history/<username>', methods=['GET'])
    def get_history(username):
        user_id = get_user_id(username)
        c.execute("SELECT city FROM history WHERE user_id=? ORDER BY id DESC", (user_id,))
        cities = c.fetchall()
        return jsonify([{"city": city[0]} for city in cities])

    @bp.route('/api/history/<username>', methods=['POST'])
    def add_history(username):
        user_id = get_user_id(username)
        data = request.json
        city = data.get("city")
        if not city:
            return jsonify({"error": "Brak miasta"}), 400
        c.execute("INSERT INTO history (user_id, city) VALUES (?, ?)", (user_id, city))
        conn.commit()
        return jsonify({"message": "Dodano do historii"})

    @bp.route('/api/history/<username>', methods=['DELETE'])
    def delete_history(username):
        user_id = get_user_id(username)
        c.execute("DELETE FROM history WHERE user_id=?", (user_id,))
        conn.commit()
        return jsonify({"message": "Historia została usunięta"})

    @bp.route('/api/default_city/<username>', methods=['POST'])
    def set_default_city(username):
        user_id = get_user_id(username)
        data = request.json
        city = data.get("city")
        if not city:
            return jsonify({"error": "Brak miasta"}), 400
        c.execute("UPDATE users SET default_city=? WHERE id=?", (city, user_id))
        conn.commit()
        return jsonify({"message": f"Ustawiono domyślne miasto na {city}"})

    @bp.route('/api/top_cities/<username>')
    def get_top_cities(username):
        limit = int(request.args.get("limit", 5))
        user_id = get_user_id(username)
        c.execute("""
            SELECT city, COUNT(*) as count 
            FROM history 
            WHERE user_id=? 
            GROUP BY city 
            ORDER BY count DESC 
            LIMIT ?
        """, (user_id, limit))
        cities = c.fetchall()
        return jsonify([city[0] for city in cities])
