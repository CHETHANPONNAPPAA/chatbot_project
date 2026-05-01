from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import os

app = Flask(__name__)
CORS(app)

# Load data
with open('intents.json') as f:
    data = json.load(f)

sentences, labels = [], []

for intent in data['intents']:
    for p in intent['patterns']:
        sentences.append(p.lower())
        labels.append(intent['tag'])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

model = LogisticRegression()
model.fit(X, labels)

@app.route('/')
def home():
    return "Chatbot API Running ✅"


@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message'].lower()

    # Get probabilities
    probs = model.predict_proba(vectorizer.transform([msg]))[0]
    max_prob = max(probs)

    # Confidence threshold (tune this)
    THRESHOLD = 0.5

    if max_prob < THRESHOLD:
        return jsonify({
            "response": "Sorry, I don't understand that 🤔. Please ask something related to AI or ML."
        })

    tag = model.classes_[probs.argmax()]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return jsonify({
                "response": random.choice(intent['responses'])
            })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))