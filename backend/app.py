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
    try:
        msg = request.json['message'].lower()
        tag = model.predict(vectorizer.transform([msg]))[0]

        for intent in data['intents']:
            if intent['tag'] == tag:
                return jsonify({"response": random.choice(intent['responses'])})

        return jsonify({"response": "I didn't understand that 🤔"})

    except Exception as e:
        print(e)
        return jsonify({"response": "Error occurred ❌"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))