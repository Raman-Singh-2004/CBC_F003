import logging
from flask import Flask, jsonify, request
import requests
import os
import uuid
import random
import re
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from songs_data import get_song_recommendations
from mental_health_analysis import analyze_text, get_mental_health_trend, format_analysis_response
from deep_listening import process_deep_thought
from mood_encouragement import process_mood
from positive_responses import process_positive_mood
from wellness_routines import process_wellness_routine_request
from therapist_contacts import process_therapist_request

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

# Store conversation history
conversation_history = {}

# Function to call Llama API (using a free API endpoint)
def get_llama_response(user_message, session_id):
    # Get or initialize conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []
        # Add system message to set the context
        conversation_history[session_id].append({
            'role': 'system',
            'content': 'You are a supportive mental health chatbot. Respond with empathy and care. ' +
                      'Provide helpful suggestions but make it clear you are not a replacement for professional help. ' +
                      'Keep responses concise and focused on the user\'s well-being.'
        })

    # Add the new user message to history
    conversation_history[session_id].append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.now().isoformat()
    })

    # Limit history to last 10 messages to prevent token limits
    if len(conversation_history[session_id]) > 10:
        # Keep the system message and the most recent messages
        conversation_history[session_id] = [conversation_history[session_id][0]] + conversation_history[session_id][-9:]

    # Check if this is a music recommendation request
    music_keywords = ['song', 'music', 'playlist', 'recommend', 'listen']
    is_music_request = any(keyword in user_message.lower() for keyword in music_keywords)

    # Analyze message for mental health concerns
    mental_health_analysis = analyze_text(user_message, session_id)
    mental_health_trend = get_mental_health_trend(session_id)
    mental_health_response = format_analysis_response(mental_health_analysis, mental_health_trend)

    # Process message for deep thoughts and generate encouraging response
    deep_thought_result = process_deep_thought(user_message)

    # Process message for negative moods and generate encouragement
    mood_result = process_mood(user_message, session_id)

    # Process message for positive moods and generate enthusiastic responses
    positive_mood_result = process_positive_mood(user_message)

    # Process message for wellness routine requests
    wellness_routine_result = process_wellness_routine_request(user_message)

    # Process message for therapist contact requests
    therapist_request_result = process_therapist_request(user_message)

    # Format conversation history for the API
    messages = []
    for msg in conversation_history[session_id]:
        if 'role' in msg and 'content' in msg:
            messages.append({"role": msg['role'], "content": msg['content']})

    # If this is a music request, handle it directly
    if is_music_request:
        reply = get_song_recommendation_response(user_message)
        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': reply,
            'timestamp': datetime.now().isoformat()
        })
        return reply

    # If therapist contact was requested, prioritize the therapist recommendations
    if therapist_request_result.get("is_therapist_request", False) and therapist_request_result.get("response"):
        therapist_response = therapist_request_result.get("response", "")

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': therapist_response,
            'timestamp': datetime.now().isoformat()
        })

        return therapist_response

    # If wellness routine was requested, prioritize the routine response
    elif wellness_routine_result.get("is_routine_request", False) and wellness_routine_result.get("response"):
        routine_response = wellness_routine_result.get("response", "")

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': routine_response,
            'timestamp': datetime.now().isoformat()
        })

        return routine_response

    # If positive mood was detected, prioritize the enthusiastic response
    elif positive_mood_result.get("has_positive_mood", False) and positive_mood_result.get("response"):
        positive_response = positive_mood_result.get("response", "")

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': positive_response,
            'timestamp': datetime.now().isoformat()
        })

        return positive_response

    # If negative mood was detected, prioritize the mood encouragement
    elif mood_result.get("has_negative_mood", False) and mood_result.get("response"):
        mood_response = mood_result.get("response", "")

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': mood_response,
            'timestamp': datetime.now().isoformat()
        })

        return mood_response

    # If deep thought was detected, prioritize the encouraging response
    elif deep_thought_result.get("is_deep_thought", False):
        deep_thought_response = deep_thought_result.get("response", "")

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': deep_thought_response,
            'timestamp': datetime.now().isoformat()
        })

        return deep_thought_response

    # If mental health concerns were detected, provide coping strategies
    elif mental_health_response:
        # Get a regular response first
        regular_reply = None
        try:
            # Try to use the API for a regular response
            api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
            headers = {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', 'hf_dummy_key')}",
                "Content-Type": "application/json"
            }

            # Format the prompt for Llama
            prompt = f"<s>[INST] <<SYS>>\nYou are a supportive mental health chatbot. Respond with empathy and care. Provide helpful suggestions but make it clear you are not a replacement for professional help. Keep responses concise and focused on the user's well-being.\n<</SYS>>\n\n{user_message} [/INST]"

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=10)

            if response.status_code == 200:
                try:
                    regular_reply = response.json()[0]["generated_text"]
                    regular_reply = regular_reply.split("[/INST]")[1].strip()
                except (KeyError, IndexError, ValueError):
                    regular_reply = fallback_response(user_message)
            else:
                regular_reply = fallback_response(user_message)
        except Exception as e:
            logging.error(f"Error calling API: {str(e)}")
            regular_reply = fallback_response(user_message)

        # Combine the regular reply with mental health coping strategies
        combined_reply = f"{regular_reply}\n\n{mental_health_response}"

        # Add the bot's reply to the conversation history
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': combined_reply,
            'timestamp': datetime.now().isoformat()
        })

        return combined_reply

    # Using HuggingFace Inference API (free tier)
    # You'll need to replace this with an actual free API endpoint
    try:
        # Try to use a free API service
        # This is a placeholder - you'll need to replace with an actual working API
        api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
        headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', 'hf_dummy_key')}",
            "Content-Type": "application/json"
        }

        # Format the prompt for Llama
        prompt = f"<s>[INST] <<SYS>>\nYou are a supportive mental health chatbot. Respond with empathy and care. Provide helpful suggestions but make it clear you are not a replacement for professional help. Keep responses concise and focused on the user's well-being. You can also suggest songs to match the user's mood if they ask for music recommendations.\n<</SYS>>\n\n{user_message} [/INST]"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }

        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            # Parse the response based on the API's format
            try:
                reply = response.json()[0]["generated_text"]
                # Extract just the assistant's reply (after the prompt)
                reply = reply.split("[/INST]")[1].strip()
            except (KeyError, IndexError, ValueError):
                # If we can't parse the response properly, use the full text
                reply = response.json()
                if isinstance(reply, list) and len(reply) > 0:
                    reply = reply[0].get("generated_text", "I'm having trouble understanding. Could you try again?")
                else:
                    reply = "I'm having trouble understanding. Could you try again?"
        else:
            # If the API call fails, fall back to the rule-based responses
            logging.error(f"API error: {response.status_code} - {response.text}")
            reply = fallback_response(user_message)

    except Exception as e:
        logging.error(f"Error calling API: {str(e)}")
        reply = fallback_response(user_message)

    # Add bot response to history
    conversation_history[session_id].append({
        'role': 'assistant',
        'content': reply,
        'timestamp': datetime.now().isoformat()
    })

    return reply

# Fallback response generator when API is unavailable
def fallback_response(message):
    message = message.lower()

    # Simple patterns for fallback responses
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    feelings = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed']
    positive_feelings = ['happy', 'joy', 'excited', 'cheerful', 'good', 'great', 'calm', 'peaceful', 'relaxed']
    jokes = ['joke', 'funny', 'laugh', 'humor']
    thanks = ['thank', 'thanks', 'appreciate']
    music_requests = ['song', 'music', 'playlist', 'recommend', 'listen']
    wellness_requests = ['routine', 'wellness', 'mental health', 'physical health', 'daily habit', 'healthy habit', 'morning routine', 'evening routine']
    therapist_requests = ['therapist', 'psychologist', 'psychiatrist', 'counselor', 'counselling', 'therapy', 'mental health professional', 'consultation', 'consultancy', 'wellness center', 'wellness centre', 'recommend therapist', 'recommend psychologist', 'recommend mental health', 'suggest therapist', 'suggest psychologist', 'mental health specialist']

    # Check for therapist contact requests
    if any(word in message for word in therapist_requests):
        therapist_result = process_therapist_request(message)
        if therapist_result.get("is_therapist_request", False) and therapist_result.get("response"):
            return therapist_result.get("response")

    # Check for wellness routine requests
    if any(word in message for word in wellness_requests):
        wellness_result = process_wellness_routine_request(message)
        if wellness_result.get("is_routine_request", False) and wellness_result.get("response"):
            return wellness_result.get("response")

    # Check for song recommendation requests
    if any(word in message for word in music_requests):
        return get_song_recommendation_response(message)

    if any(word in message for word in greetings):
        return random.choice([
            "Hello! How are you feeling today?",
            "Hi there! How can I support you today?",
            "Hey! What's on your mind?"
        ])

    # Check for feelings to suggest songs
    for feeling in feelings + positive_feelings:
        if feeling in message:
            # Get song recommendations for this feeling
            songs = get_song_recommendations(feeling, count=2)
            if songs:
                song_text = format_song_recommendations(songs, feeling)
                return f"I notice you're feeling {feeling}. {random.choice([
                    'Music can help with your mood.',
                    'Sometimes music can be therapeutic.',
                    'The right song might help you process these feelings.'
                ])} {song_text}"

    if any(word in message for word in feelings):
        return random.choice([
            "I'm sorry to hear you're feeling that way. Would you like to talk more about it? I could also suggest some songs that might help.",
            "That sounds tough. Remember, it's okay to feel this way. Would you like me to recommend some music that might resonate with you?",
            "Have you tried any strategies to help you feel better? Music can be therapeutic - I can suggest some songs if you'd like."
        ])

    if any(word in message for word in jokes):
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? It was two-tired!"
        ])

    if any(word in message for word in thanks):
        return "You're welcome! I'm here whenever you need to talk."

    # Default response
    return "Thanks for sharing. Remember, talking about your feelings can help. I can also suggest songs to match your mood if you'd like - just ask for music recommendations."

# Function to handle song recommendation requests
def get_song_recommendation_response(message):
    # Try to extract mood from the message
    mood_patterns = [
        r"(?:i(?:'m| am) feeling|i feel|make me feel|when i(?:'m| am)) (\w+)",
        r"(?:recommend|suggest) (?:some|a few|) (?:songs|music) (?:for|when) (?:i(?:'m| am) feeling |i feel |feeling |)(\w+)",
        r"(?:songs|music) (?:for|when) (?:i(?:'m| am)|one is) (\w+)",
        r"(?:i want to|i need to|help me) (?:feel|be) (\w+)",
        r"(?:i(?:'m| am)|i want to be) in a (\w+) mood"
    ]

    # Try to extract mood using patterns
    mood = None
    for pattern in mood_patterns:
        match = re.search(pattern, message.lower())
        if match:
            mood = match.group(1)
            break

    # If no mood found, check for common mood words
    if not mood:
        mood_words = [
            "happy", "sad", "calm", "energetic", "focused", "relaxed",
            "joy", "excited", "cheerful", "depressed", "unhappy", "peaceful",
            "active", "motivated", "concentrated", "chill", "mellow"
        ]
        for word in mood_words:
            if word in message.lower():
                mood = word
                break

    # If still no mood found, ask for clarification
    if not mood:
        return "I'd be happy to suggest some songs! What kind of mood are you in or what mood would you like to enhance? For example, happy, sad, calm, energetic, focused, or relaxed?"

    # Get song recommendations for the mood
    songs = get_song_recommendations(mood, count=3)

    # If no songs found for this mood, give a generic response
    if not songs:
        return f"I don't have specific song recommendations for a {mood} mood, but I can suggest songs for happy, sad, calm, energetic, focused, or relaxed moods. Let me know which you'd prefer!"

    # Format the song recommendations
    return format_song_recommendations(songs, mood)

# Function to format song recommendations
def format_song_recommendations(songs, mood):
    if not songs:
        return "I don't have any specific song recommendations at the moment."

    # Create the response text
    response = f"Here are some songs that might amplify your {mood} mood:\n\n"

    for i, song in enumerate(songs, 1):
        response += f"{i}. \"{song['title']}\" by {song['artist']}\n"
        response += f"   Listen: {song['link']}\n\n"

    response += "I hope these songs help enhance your mood! Let me know if you'd like more recommendations."
    return response

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

        # Call the Llama API
        reply = get_llama_response(user_message, session_id)
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
    logging.basicConfig(level=logging.INFO)  # Set up logging
    app.run(host="0.0.0.0", port=5000)  # Run the app
