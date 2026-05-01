from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)

# Load data
with open('intents.json') as f:
    data = json.load(f)

patterns = []
tags = []

for intent in data['intents']:
    for p in intent['patterns']:
        patterns.append(p.lower())
        tags.append(intent['tag'])

# ✅ Better vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

@app.route('/')
def home():
    return "Chatbot API Running ✅"


@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message'].lower().strip()

    # ✅ 1. Handle simple intents
    simple_map = {
        "hi": "greeting",
        "hello": "greeting",
        "hey": "greeting",
        "bye": "goodbye",
        "thanks": "thanks",
        "thank you": "thanks"
    }

    if msg in simple_map:
        tag = simple_map[msg]
        for intent in data['intents']:
            if intent['tag'] == tag:
                return jsonify({
                    "response": random.choice(intent['responses'])
                })

    # ✅ 2. Similarity matching (REPLACES ML MODEL)
    msg_vec = vectorizer.transform([msg])
    similarity = cosine_similarity(msg_vec, X)[0]

    max_index = similarity.argmax()
    max_score = similarity[max_index]

    THRESHOLD = 0.4

    if max_score < THRESHOLD:
        return jsonify({
            "response": "Sorry, I don't understand that 🤔. Ask something related to AI or ML."
        })

    tag = tags[max_index]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return jsonify({
                "response": random.choice(intent['responses'])
            })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))