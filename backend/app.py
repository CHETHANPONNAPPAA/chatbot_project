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

    # 🔹 1. Handle simple intents (greetings etc.)
    simple_map = {
        "hi": "greeting",
        "hello": "greeting",
        "hey": "greeting",
        "bye": "goodbye",
        "thanks": "thanks",
        "thank you": "thanks"
    }

    for key in simple_map:
        if key in msg:
            tag = simple_map[key]
            for intent in data['intents']:
                if intent['tag'] == tag:
                    return jsonify({
                        "response": random.choice(intent['responses'])
                    })

    # 🔹 2. Similarity matching
    msg_vec = vectorizer.transform([msg])
    similarity = cosine_similarity(msg_vec, X)[0]

    max_index = similarity.argmax()
    max_score = similarity[max_index]

    tag = tags[max_index]
    pattern_text = patterns[max_index]

    # 🔹 3. Remove common words (VERY IMPORTANT)
    stop_words = {"what", "is", "the", "a", "an", "tell", "me", "about"}

    msg_words = set(msg.split()) - stop_words
    pattern_words = set(pattern_text.split()) - stop_words

    common_words = msg_words & pattern_words

    # 🔹 4. Threshold check
    THRESHOLD = 0.4

    if max_score < THRESHOLD or len(common_words) == 0:
        return jsonify({
            "response": "Sorry, I don't understand that 🤔. Ask something related to AI or ML."
        })

    # 🔹 5. Return response
    for intent in data['intents']:
        if intent['tag'] == tag:
            return jsonify({
                "response": random.choice(intent['responses'])
            })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))