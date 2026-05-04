from flask import Flask, request, jsonify, g
from flask_cors import CORS
import json, random, sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            "users.db",
            timeout=10,
            check_same_thread=False
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA synchronous=NORMAL")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect("users.db")
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    db.commit()
    db.close()

init_db()

# ================= LOAD CHATBOT =================
with open('intents.json') as f:
    data = json.load(f)

patterns = []
tags = []

for intent in data['intents']:
    for p in intent['patterns']:
        patterns.append(p.lower())
        tags.append(intent['tag'])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

# ================= AUTH =================

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    try:
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return jsonify({"message": "User registered ✅"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists ❌"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


# ================= CHAT =================

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message'].lower().strip()

    simple_map = {
        "hi": "greeting",
        "hello": "greeting",
        "bye": "goodbye",
        "thanks": "thanks"
    }

    for key in simple_map:
        if key in msg:
            tag = simple_map[key]
            for intent in data['intents']:
                if intent['tag'] == tag:
                    return jsonify({"response": random.choice(intent['responses'])})

    msg_vec = vectorizer.transform([msg])
    similarity = cosine_similarity(msg_vec, X)[0]

    max_index = similarity.argmax()
    max_score = similarity[max_index]

    tag = tags[max_index]
    pattern_text = patterns[max_index]

    stop_words = {"what", "is", "the", "a", "an", "tell", "me"}
    msg_words = set(msg.split()) - stop_words
    pattern_words = set(pattern_text.split()) - stop_words

    if max_score < 0.4 or len(msg_words & pattern_words) == 0:
        return jsonify({"response": "Sorry, I don't understand 🤔"})

    for intent in data['intents']:
        if intent['tag'] == tag:
            return jsonify({"response": random.choice(intent['responses'])})


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))