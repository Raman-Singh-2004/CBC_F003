import logging
from flask import Flask, jsonify, request
import requests
import os
import uuid
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Configure CORS to allow requests from any origin
CORS(app,
     supports_credentials=True,  # Enable CORS with credentials support
     resources={r"/*": {"origins": "*"}},  # Allow all origins
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "OPTIONS"]
)

# Function to call OpenAI API
def get_chatgpt_response(user_message):
    api_key = os.getenv('OPENAI_API_KEY')  # Use environment variable for API key

    if not api_key:
        logging.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return "I'm sorry, but I'm not configured correctly. Please contact the administrator."
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    # Store conversation history in a dictionary with session IDs as keys
    conversation_history = getattr(app, 'conversation_history', {})

    # Get or create session ID from request
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())

    # Get or initialize conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []
        # Add system message to set the context for the AI
        conversation_history[session_id].append({
            'role': 'system',
            'content': 'You are a supportive mental health chatbot. Respond with empathy and care. ' +
                      'Provide helpful suggestions but make it clear you are not a replacement for professional help. ' +
                      'Keep responses concise and focused on the user\'s well-being.'
        })

    # Add the new user message to history
    conversation_history[session_id].append({'role': 'user', 'content': user_message})

    # Limit history to last 10 messages to prevent token limits
    if len(conversation_history[session_id]) > 10:
        # Keep the system message and the most recent messages
        conversation_history[session_id] = [conversation_history[session_id][0]] + conversation_history[session_id][-9:]

    # Save the conversation history back to the app
    app.conversation_history = conversation_history

    # Prepare the messages for the API call
    data = {
        'model': 'gpt-3.5-turbo',  # Use the appropriate model
        'messages': conversation_history[session_id],
        'max_tokens': 150,  # Adjust as needed
        'temperature': 0.7  # Add some variability but keep responses focused
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({'role': 'assistant', 'content': reply})
        return reply
    else:
        logging.error(f"OpenAI API error: {response.status_code} - {response.text}")

        # Check for specific error types
        try:
            error_data = response.json().get('error', {})
            error_type = error_data.get('type', '')
            error_message = error_data.get('message', '')

            if error_type == 'insufficient_quota':
                # Fallback to a simple response generator when API quota is exceeded
                return fallback_response(user_message)
            else:
                return f"API Error: {error_message}"
        except:
            return "Sorry, I couldn't process your request at the moment. The OpenAI API is currently unavailable."

# Fallback response generator when API is unavailable
def fallback_response(message):
    message = message.lower()

    # Simple patterns for fallback responses
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    feelings = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed']
    jokes = ['joke', 'funny', 'laugh', 'humor']
    thanks = ['thank', 'thanks', 'appreciate']

    if any(word in message for word in greetings):
        return random.choice([
            "Hello! I'm currently using a fallback system as the AI service is unavailable. How can I help you today?",
            "Hi there! The AI service is currently down, but I can still chat with you using my basic responses.",
            "Hey! I'm operating in fallback mode right now, but I'm still here to help!"
        ])

    if any(word in message for word in feelings):
        return random.choice([
            "I'm sorry to hear you're feeling that way. Remember that it's okay to seek help when you need it.",
            "That sounds difficult. Even though I'm in fallback mode, I want you to know that your feelings are valid.",
            "I understand this is hard. Consider reaching out to a mental health professional who can provide proper support."
        ])

    if any(word in message for word in jokes):
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I'm currently in fallback mode, but here's a joke: Why did the bicycle fall over? It was two-tired!"
        ])

    if any(word in message for word in thanks):
        return "You're welcome! I'm happy to help, even in fallback mode."

    # Default response
    return "I'm currently operating in fallback mode because the AI service is unavailable. I have limited responses, but I'm still here to chat!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Log request details for debugging
        logging.info(f"Received request: {request.method} {request.path}")
        logging.info(f"Request headers: {dict(request.headers)}")

        data = request.get_json()
        logging.info(f"Request data: {data}")

        user_message = data.get('message', '').strip()
        logging.info(f"User message: {user_message}")

        if not user_message:
            return jsonify({'reply': "Please provide a message."}), 400

        # Get or create session ID
        session_id = request.cookies.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            logging.info(f"Created new session ID: {session_id}")
        else:
            logging.info(f"Using existing session ID: {session_id}")

        # Call the OpenAI API
        reply = get_chatgpt_response(user_message)
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Set up logging
    app.run(host="0.0.0.0", port=5000)  # Run the app

