import json, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

with open('intents.json') as f:
    data = json.load(f)

sentences, labels = [], []

for intent in data['intents']:
    for p in intent['patterns']:
        sentences.append(p)
        labels.append(intent['tag'])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

model = LogisticRegression()
model.fit(X, labels)

def get_response(text):
    tag = model.predict(vectorizer.transform([text]))[0]
    for intent in data['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])