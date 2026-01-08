from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random
import datetime

app = Flask(__name__)
CORS(app)

last_question = ""
last_topic = ""

# ---------------- SAFE MATH ----------------
def solve_math(text):
    try:
        text = text.replace("×", "*").replace("÷", "/")
        if re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", text):
            return str(eval(text))
    except:
        return None

# ---------------- TRANSLATION (DEMO) ----------------
hi_to_en = {
    "tum kaun ho": "Who are you?",
    "tum kaise ho": "How are you?",
    "paisa kaise kamaye": "How to earn money?",
    "aaj kya karu": "What should I do today?"
}

en_to_hi = {
    "who are you": "तुम कौन हो?",
    "how are you": "तुम कैसे हो?",
    "how to earn money": "पैसा कैसे कमाएँ?",
    "what should i do today": "आज मुझे क्या करना चाहिए?"
}

def translate(text):
    t = text.lower().strip()
    if t in hi_to_en:
        return f"English Translation:\n{hi_to_en[t]}"
    if t in en_to_hi:
        return f"Hindi Translation:\n{en_to_hi[t]}"
    return None

# ---------------- HUMAN HELPERS ----------------
def confident_opening():
    return random.choice([
        "That’s a thoughtful question.",
        "Good point — many people think about this.",
        "You’re asking something meaningful."
    ])

def professional_close():
    return random.choice([
        "If you’d like, I can explain this with an example.",
        "Let me know if you want a practical perspective.",
        "Happy to go deeper into this."
    ])

# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    global last_question, last_topic

    data = request.get_json()
    q = data.get("message", "").strip()

    if not q:
        return jsonify({"reply": "Please ask something 🙂"})

    ql = q.lower()

    # --------- MATH ---------
    math_ans = solve_math(ql)
    if math_ans:
        last_topic = "math"
        last_question = q
        return jsonify({"reply": f"✅ Math Answer: {math_ans}"})

    # --------- TRANSLATION ---------
    trans = translate(q)
    if trans:
        last_topic = "translation"
        last_question = q
        return jsonify({"reply": trans})

    # --------- INTRO / ABOUT ---------
    if any(p in ql for p in ["introduce yourself", "about you", "tell me about you", "who are you"]):
        reply = (
            "I’m **ShivX**, a human-like AI assistant created by **Shiv**.\n\n"
            "I’m designed to answer questions the way a thoughtful human would — "
            "clearly, practically, and without unnecessary complexity.\n\n"
            "I can help with everyday questions, logical thinking, basic math, "
            "Hindi–English translation, and professional discussions.\n\n"
            "This is a demo system built without paid AI APIs, focused on realistic conversation."
        )

    # --------- GREETING ---------
    elif any(w in ql for w in ["hi", "hello", "hey"]):
        reply = (
            "Hello 👋 I’m ShivX.\n"
            "You can ask me about life, learning, math, or general ideas."
        )

    # --------- WHAT ARE YOU DOING ---------
    elif "what are you doing" in ql:
        reply = (
            "I’m here to understand questions and respond thoughtfully — "
            "just like a calm, focused human would."
        )

    # --------- HOW ARE YOU ---------
    elif "how are you" in ql:
        reply = "I’m doing well, thank you. What would you like to talk about?"

    # --------- TIME ---------
    elif "time" in ql:
        now = datetime.datetime.now().strftime("%A, %I:%M %p")
        reply = f"It’s currently {now}."

    # --------- CAREER / LINKEDIN ---------
    elif any(w in ql for w in ["career", "job", "linkedin", "future"]):
        reply = (
            "Career growth usually comes from three things:\n"
            "clarity, consistency, and continuous learning.\n\n"
            "People who focus on long-term improvement tend to do better than "
            "those chasing shortcuts."
        )

    # --------- LIFE / MOTIVATION ---------
    elif any(w in ql for w in ["life", "stress", "sad", "motivation", "failure"]):
        reply = (
            "Life feels uncertain at times — that’s completely normal.\n\n"
            "Clarity often comes after taking action, not before."
        )

    # --------- FOLLOW-UP ---------
    elif last_question and any(w in ql for w in ["and", "then", "more", "next"]):
        reply = (
            f"You’re continuing the same topic 👍\n"
            f"Earlier you asked: “{last_question}”.\n"
            "What would you like to explore next?"
        )

    # --------- DEFAULT SMART ---------
    else:
        reply = (
            f"{confident_opening()}\n"
            "A practical way to think about this is to stay logical and focused.\n"
            f"{professional_close()}"
        )

    last_question = q
    last_topic = "general"
    return jsonify({"reply": reply})


@app.route("/")
def home():
    return "ShivX backend running (ADVANCED ENGLISH DEMO MODE)"

app.run(host="127.0.0.1", port=5000, debug=True)
