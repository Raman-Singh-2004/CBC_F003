from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import logging
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend JS to access backend

# Set up logging
logging.basicConfig(level=logging.INFO)

# Simple rules-based response logic for mental health chatbot
def generate_response(message):
    message = message.lower()

    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    feelings = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed']
    
    if any(greet in message for greet in greetings):
        return random.choice([
            "Hello! How are you feeling today?",
            "Hi there! How can I support you today?",
            "Hey! What's on your mind?"
        ])

    if any(feel in message for feel in feelings):
        return random.choice([
            "I'm sorry to hear that. Would you like to talk more about it?",
            "That sounds tough. Remember, it's okay to feel this way.",
            "Have you tried any strategies to help you feel better?"
        ])

    if 'help' in message:
        return "I'm here to listen. Please share what you're feeling."

    if 'thank' in message or 'thanks' in message:
        return "You're welcome! I'm here whenever you need to talk."

    # Default fallback response
    return ("Thanks for sharing. Remember, talking about your feelings can help. "
            "If you feel overwhelmed, consider reaching out to a mental health professional.")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        reply = generate_response(user_message)
        return jsonify({'reply': reply})
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'reply': "Sorry, I couldn't process your request. Please try again."}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


