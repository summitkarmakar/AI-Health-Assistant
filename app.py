from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Load dataset
data = pd.read_csv("Symptom2Disease.CSV")

print(data.head())
print("Dataset loaded successfully")

# Dataset columns
X = data["text"]
y = data["label"]

# Convert text to numeric
vectorizer = CountVectorizer()
X_vector = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vector, y)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# AI Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    data_json = request.get_json()
    symptom = data_json["symptom"]

    vector = vectorizer.transform([symptom])
    prediction = model.predict(vector)

    return jsonify({"disease": prediction[0]})


if __name__ == "__main__":
    app.run(debug=True)