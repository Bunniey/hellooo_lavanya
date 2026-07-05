from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "lavanya-quiz-secret"

QUESTIONS = {
    "identity": "I know you're Pahadi and from South Delhi, but what would you like to be called as?",
    "normalFood": "I like to eat on normal days?",
    "specialFood": "I like to spice up my special days from?",
    "lifelongFood": "If I ask you what food you could eat for the rest of your life, then what would it be?",
    "foodType": "FOOD Department se last question.....",
    "foodNote": "If you want to express more about food, write here...",
    "flower": "I like..... my fav flower",
    "genre": "Now let's know about music taste!! Pick your fav genre",
    "artist": "My fav music artist...",
    "spotify": "Spotify account",
    "drink": "I'm a coffee person or a chai person?",
    "hobbies": "Let's know about your hobbies now....",
    "hobbyOther": "If other, mention it here...",
    "scroll": "I like to scroll...",
    "feedback": "How did you like this?",
    "feedbackNote": "Tell me your honest feelings..."
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    data = request.form.to_dict(flat=True)
    rows = []
    for key, question in QUESTIONS.items():
        if key in data and data[key].strip():
            rows.append({
                "question": question,
                "answer": data[key].strip()
            })
    return render_template("result.html", rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
