from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import logging
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configure CORS to allow requests from any origin
CORS(app,
     supports_credentials=True,  # Enable CORS with credentials support
     resources={r"/*": {"origins": "*"}},  # Allow all origins
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "OPTIONS"]
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Store conversation history
conversation_history = {}

# Simple rules-based response logic for mental health chatbot
def generate_response(message, session_id):
    message = message.lower()

    # Get or create conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    # Add user message to history
    conversation_history[session_id].append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    })

    # Limit history to last 10 messages to prevent memory issues
    if len(conversation_history[session_id]) > 10:
        conversation_history[session_id] = conversation_history[session_id][-10:]

    # Check for patterns in the message
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    feelings = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed']

    # Check if this is a follow-up question
    is_followup = len(conversation_history[session_id]) > 2

    # Generate appropriate response based on context
    response = ""

    if any(greet in message for greet in greetings):
        response = random.choice([
            "Hello! How are you feeling today?",
            "Hi there! How can I support you today?",
            "Hey! What's on your mind?"
        ])
    elif any(feel in message for feel in feelings):
        if is_followup and any(feel in conversation_history[session_id][-3]['content'] for feel in feelings):
            # If user mentioned feelings before, provide a deeper response
            response = random.choice([
                "You've mentioned feeling this way before. Has anything changed since we last talked?",
                "I notice you're still feeling this way. Would it help to explore some coping strategies?",
                "It sounds like these feelings are persistent. Have you considered speaking with a mental health professional?"
            ])
        else:
            response = random.choice([
                "I'm sorry to hear that. Would you like to talk more about it?",
                "That sounds tough. Remember, it's okay to feel this way.",
                "Have you tried any strategies to help you feel better?"
            ])
    elif 'help' in message:
        response = "I'm here to listen. Please share what you're feeling."
    elif 'thank' in message or 'thanks' in message:
        response = "You're welcome! I'm here whenever you need to talk."
    else:
        # Default fallback response
        response = ("Thanks for sharing. Remember, talking about your feelings can help. "
                "If you feel overwhelmed, consider reaching out to a mental health professional.")

    # Add bot response to history
    conversation_history[session_id].append({
        'role': 'bot',
        'content': response,
        'timestamp': datetime.now().isoformat()
    })

    return response

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Log request details for debugging
        logging.info(f"Received request: {request.method} {request.path}")
        logging.info(f"Request headers: {dict(request.headers)}")

        data = request.get_json()
        logging.info(f"Request data: {data}")

        user_message = data.get('message', '')
        logging.info(f"User message: {user_message}")

        # Get or create session ID
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            logging.info(f"Created new session ID: {session_id}")
        else:
            logging.info(f"Using existing session ID: {session_id}")

        # Generate response based on message and conversation history
        reply = generate_response(user_message, session_id)
        logging.info(f"Generated reply: {reply}")

        # Create response with session cookie
        response = jsonify({'reply': reply})
        response.set_cookie('session_id', session_id, max_age=86400)  # 24 hour expiry

        # Add CORS headers explicitly
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        logging.info(f"Sending response: {response.data}")
        return response
    except Exception as e:
        logging.error(f"Error processing request: {e}", exc_info=True)
        error_response = jsonify({'reply': f"Sorry, I couldn't process your request. Error: {str(e)}"})

        # Add CORS headers to error response too
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        error_response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        error_response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        error_response.headers.add('Access-Control-Allow-Credentials', 'true')

        return error_response, 400

# Add OPTIONS method handler for CORS preflight requests
@app.route('/chat', methods=['OPTIONS'])
def handle_options():
    response = app.make_default_options_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Clean up old conversations periodically
@app.before_request
def cleanup_old_sessions():
    # This is a simple cleanup that runs before each request
    # In a production app, you'd want to do this in a background task
    current_time = datetime.now()
    sessions_to_remove = []

    for session_id, history in conversation_history.items():
        if history:
            last_message_time = datetime.fromisoformat(history[-1]['timestamp'])
            # Remove sessions older than 24 hours
            if (current_time - last_message_time).total_seconds() > 86400:
                sessions_to_remove.append(session_id)

    for session_id in sessions_to_remove:
        del conversation_history[session_id]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

