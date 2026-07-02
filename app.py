from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# 🧠 session memory
chat_memory = []
mood_score = 0  # -5 (bad) to +5 (good)


@app.route("/")
def home():
    return render_template("index.html")


def analyze_mood(message):
    global mood_score

    msg = message.lower()

    if any(w in msg for w in ["sad", "depressed", "lonely", "cry", "hurt"]):
        mood_score -= 1
    elif any(w in msg for w in ["stress", "anxious", "worried", "panic"]):
        mood_score -= 1
    elif any(w in msg for w in ["happy", "good", "great", "excited"]):
        mood_score += 1
    elif any(w in msg for w in ["motivate", "better", "hope"]):
        mood_score += 1

    # clamp range
    mood_score = max(-5, min(5, mood_score))


def generate_session_summary():
    if mood_score <= -3:
        return (
            "📊 Session Insight:\n\n"
            "You seemed to be carrying a heavy emotional load today. "
            "Your responses reflected stress, sadness, or overwhelm.\n\n"
            "💡 Suggestion: Try slowing down your thoughts and focusing on grounding techniques."
        )

    elif -2 <= mood_score <= 2:
        return (
            "📊 Session Insight:\n\n"
            "Your emotional state seemed mixed and stable overall. "
            "Some fluctuations in mood were observed.\n\n"
            "💡 Suggestion: Keep observing your thoughts without judging them."
        )

    else:
        return (
            "📊 Session Insight:\n\n"
            "You showed a generally positive emotional pattern today 🌿\n\n"
            "💡 Suggestion: Maintain this momentum by engaging in activities you enjoy."
        )



chat_memory = []

def summarize_memory():
    """Creates a simple 'context feeling' from conversation history"""
    if len(chat_memory) < 2:
        return "first interaction"

    last_msgs = " ".join(chat_memory[-6:]).lower()

    if any(w in last_msgs for w in ["sad", "depressed", "cry", "lonely"]):
        return "user is emotionally low and needs comfort"

    if any(w in last_msgs for w in ["stress", "anxious", "panic", "worried"]):
        return "user is mentally overwhelmed"

    if any(w in last_msgs for w in ["happy", "good", "excited"]):
        return "user is in positive emotional state"

    return "neutral conversation"


def get_ai_response(user_message):
    global chat_memory

    msg = user_message.strip()
    lower_msg = msg.lower()

    chat_memory.append(msg)
    chat_memory = chat_memory[-12:]

    context = summarize_memory()

    # 🎭 human-style openings (varied tone)
    openers = [
        "I hear you…",
        "I get what you're saying…",
        "Hmm… I’m listening.",
        "That sounds real.",
        "I’m here with you on this."
    ]

    def reply(text):
        return f"{random.choice(openers)}\n\n{text}"

    # 🧠 CONTEXT + RESPONSE GENERATION

    if context == "user is emotionally low and needs comfort":
        return reply(
            "you’ve been carrying something heavy, haven’t you?\n\n"
            "You don’t have to explain it perfectly… just tell me what hurts the most right now."
        )

    elif context == "user is mentally overwhelmed":
        return reply(
            "it feels like your mind hasn’t slowed down in a while.\n\n"
            "If you had to pick one thought that’s bothering you the most, what would it be?"
        )

    elif context == "user is in positive emotional state":
        return reply(
            "I like this energy in you.\n\n"
            "What do you think made things feel better today?"
        )

    # 🔥 natural conversation continuation (MOST IMPORTANT)
    else:
        return reply(
            "go on… I’m listening.\n\n"
            "Say it the way it comes to your mind, no pressure."
        )
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    reply = get_ai_response(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)