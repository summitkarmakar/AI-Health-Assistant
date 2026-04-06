from flask import Flask, render_template, request, jsonify, redirect, session
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)
app.secret_key = "supersecretkey"   # 🔐 required for session

# =========================
# DATABASE (LOGIN SYSTEM)
# =========================

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("data/dataset.csv")   # ⚠️ ensure correct path

data = data.fillna("")

# Combine symptoms into single text
symptom_columns = data.columns[1:]
data["text"] = data[symptom_columns].apply(lambda x: " ".join(x), axis=1)

X = data["text"]
y = data["Disease"]

print("Dataset Loaded ✅")

# =========================
# MODEL TRAINING
# =========================

vectorizer = CountVectorizer()
X_vector = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vector, y)

print("Model Trained ✅")

# =========================
# ROUTES
# =========================

# 🔐 Protected Home Page
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login-page")
    return render_template("index.html")

# Login Page
@app.route("/login-page")
def login_page():
    if "user" in session:
        return redirect("/")   # already logged in
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login-page")

# =========================
# LOGIN API
# =========================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()

    conn.close()

    if user:
        session["user"] = username   # ✅ session start
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})

# =========================
# AI PREDICTION
# =========================

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return jsonify({"disease": "Please login first"})

    data_json = request.get_json()
    symptom = data_json["symptom"]

    vector = vectorizer.transform([symptom])
    prediction = model.predict(vector)

    return jsonify({"disease": prediction[0]})

# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)