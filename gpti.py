import logging
from flask import Flask, jsonify, request
import requests
import os
import uuid
import random
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

# Function to generate responses (using enhanced fallback responses)
def get_chatgpt_response(user_message):
    # Store conversation history in a dictionary with session IDs as keys
    conversation_history = getattr(app, 'conversation_history', {})

    # Get or create session ID from request
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())

    # Get or initialize conversation history for this session
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    # Add the new user message to history
    conversation_history[session_id].append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.now().isoformat()
    })

    # Limit history to last 10 messages
    if len(conversation_history[session_id]) > 10:
        conversation_history[session_id] = conversation_history[session_id][-10:]

    # Save the conversation history back to the app
    app.conversation_history = conversation_history

    # Generate a response using our enhanced rule-based system
    reply = enhanced_response(user_message, session_id)

    # Add the bot's reply to the conversation history
    conversation_history[session_id].append({
        'role': 'assistant',
        'content': reply,
        'timestamp': datetime.now().isoformat()
    })

    return reply

# Enhanced response generator with more sophisticated patterns
def enhanced_response(message, session_id=None):
    message = message.lower()

    # Expanded patterns for better response matching
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'greetings', 'what\'s up']
    feelings_negative = ['sad', 'depressed', 'unhappy', 'stress', 'anxiety', 'lonely', 'tired', 'angry', 'worried', 'overwhelmed', 'exhausted', 'frustrated', 'upset', 'down', 'miserable', 'hopeless']
    feelings_positive = ['happy', 'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'joyful', 'excited', 'content', 'peaceful', 'relaxed', 'cheerful', 'delighted', 'pleased']
    jokes = ['joke', 'funny', 'laugh', 'humor', 'comedy', 'amuse', 'entertain']
    thanks = ['thank', 'thanks', 'appreciate', 'grateful', 'gratitude']
    music = ['song', 'music', 'playlist', 'recommend', 'listen', 'tune', 'melody', 'artist', 'band', 'album', 'track']
    help_requests = ['help', 'advice', 'suggestion', 'guidance', 'assist', 'support', 'tip', 'recommendation']
    wellness = ['routine', 'wellness', 'mental health', 'physical health', 'daily habit', 'healthy habit', 'morning routine', 'evening routine', 'meditation', 'exercise', 'sleep', 'diet', 'nutrition']
    wellness_centers = ['wellness center', 'wellness centre', 'mental health center', 'mental health clinic', 'healing center', 'holistic center', 'mindfulness center', 'meditation center', 'yoga studio', 'health spa']
    therapist = ['therapist', 'psychologist', 'psychiatrist', 'counselor', 'counselling', 'therapy', 'mental health professional', 'consultation', 'consultancy']

    # Check for song recommendations
    if any(word in message for word in music):
        return random.choice([
            "I'd love to suggest some songs! For a happy mood, try 'Happy' by Pharrell Williams or 'Can't Stop the Feeling' by Justin Timberlake. For a more relaxed vibe, 'Weightless' by Marconi Union is wonderful.",
            "Music can be so therapeutic! If you're feeling down, 'Fix You' by Coldplay might resonate. For an energy boost, 'Don't Stop Me Now' by Queen is perfect!",
            "Here are some song recommendations: For focus, try 'Experience' by Ludovico Einaudi. For relaxation, 'Somewhere Over The Rainbow' by Israel Kamakawiwo'ole is beautiful.",
            "I'd recommend 'Walking on Sunshine' by Katrina & The Waves to lift your spirits, or 'Breathe' by Télépopmusik for a calming effect."
        ])

    # Check for wellness center requests first (more specific than general wellness)
    if any(center in message for center in wellness_centers):
        return """Here are some recommended wellness centers that provide mental health services:

1. **Mindful Healing Center**
   - Address: 1270 Avenue of the Americas, Suite 1505, New York, NY 10020
   - Services: Therapy, Meditation Classes, Stress Management Workshops
   - Contact: (212) 555-7890
   - Website: www.mindfulhealingcenter.com

2. **Wellness Renewal Institute**
   - Address: 450 Sutter Street, Suite 840, San Francisco, CA 94108
   - Services: Holistic Mental Health, Yoga, Nutrition Counseling
   - Contact: (415) 555-3421
   - Website: www.wellnessrenewal.org

3. **Serenity Wellness Collective**
   - Address: 11500 W. Olympic Blvd, Suite 400, Los Angeles, CA 90064
   - Services: Group Therapy, Mindfulness Training, Art Therapy
   - Contact: (310) 555-9876
   - Website: www.serenitywellness.com

4. **Harmony Health Center**
   - Address: 211 E. Ontario Street, Suite 1100, Chicago, IL 60611
   - Services: Mental Health Counseling, Meditation, Wellness Workshops
   - Contact: (312) 555-4567
   - Website: www.harmonyhealthcenter.org

5. **Tranquil Mind Wellness**
   - Address: 1330 Boylston Street, Suite 500, Boston, MA 02215
   - Services: Therapy, Yoga, Meditation, Stress Reduction Programs
   - Contact: (617) 555-2345
   - Website: www.tranquilmindwellness.com"""

    # Check for wellness routine requests
    if any(word in message for word in wellness):
        return random.choice([
            "Here's a simple morning wellness routine: 1) Start with 5 minutes of deep breathing or meditation. 2) Drink a glass of water. 3) Stretch for 5-10 minutes. 4) Write down 3 things you're grateful for. 5) Eat a nutritious breakfast.",
            "For mental wellness, try this daily routine: 1) Practice mindfulness for 10 minutes. 2) Take short breaks throughout your day. 3) Go for a 15-minute walk outdoors. 4) Connect with a loved one. 5) Before bed, reflect on 3 positive moments from your day.",
            "A balanced daily wellness routine might include: 1) 7-8 hours of quality sleep. 2) Staying hydrated throughout the day. 3) 30 minutes of physical activity. 4) Eating nutritious meals. 5) 15 minutes of relaxation or hobby time. 6) Limited screen time before bed.",
            "For an evening wind-down routine, try: 1) Disconnect from screens 1 hour before bed. 2) Take a warm shower or bath. 3) Practice gentle stretching. 4) Write in a journal or read a book. 5) Do a brief meditation or deep breathing exercise."
        ])

    # Check for therapist recommendations
    if any(word in message for word in therapist):
        return "If you're looking for professional mental health support, here are some options: 1) Dr. Jennifer Reynolds, Licensed Clinical Psychologist (212-555-7890), specializing in anxiety and depression. 2) Sophia Rodriguez, LMFT (310-555-9876), focusing on relationship issues. 3) David Kim, LCSW (206-555-7654), specializing in trauma recovery. You can also use online directories like Psychology Today or BetterHelp to find therapists in your area."

    # Check for greetings
    if any(word in message for word in greetings):
        return random.choice([
            "Hello! I'm happiRay, your mental health companion. How are you feeling today?",
            "Hi there! I'm here to chat and support you. What's on your mind?",
            "Hey! I'm happiRay. I'm here to listen and help however I can. How are you doing?",
            "Greetings! I'm your friendly mental health chatbot. How can I support you today?"
        ])

    # Check for positive feelings
    if any(word in message for word in feelings_positive):
        return random.choice([
            "That's wonderful to hear! It's so important to acknowledge and celebrate positive feelings. What's contributing to your good mood?",
            "I'm so happy to hear you're feeling good! Those positive emotions are worth savoring. Would you like to share what's going well?",
            "That's fantastic! Your positive energy is contagious. What's bringing you joy today?",
            "It's great that you're feeling positive! These good moments are precious. Is there anything specific that's brightened your day?"
        ])

    # Check for negative feelings
    if any(word in message for word in feelings_negative):
        return random.choice([
            "I'm sorry to hear you're feeling that way. Your feelings are valid, and it takes courage to express them. Would you like to talk more about what's going on?",
            "It sounds like you're going through a difficult time. Remember that it's okay to not be okay sometimes. Is there anything specific that's troubling you?",
            "I hear you, and I want you to know that you're not alone in feeling this way. Many people experience similar emotions. Would it help to talk about what might be causing these feelings?",
            "Thank you for sharing how you're feeling. That can be hard to do. Remember that difficult emotions are part of being human, and they do pass with time. Is there something I can do to support you right now?"
        ])

    # Check for jokes
    if any(word in message for word in jokes):
        return random.choice([
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? It was two-tired!",
            "What do you call a fake noodle? An impasta!",
            "How does a penguin build its house? Igloos it together!",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ])

    # Check for thanks
    if any(word in message for word in thanks):
        return random.choice([
            "You're very welcome! I'm here whenever you need to talk.",
            "It's my pleasure to be here for you. How else can I help?",
            "I'm glad I could be of assistance. Remember, I'm here anytime you need support.",
            "You're welcome! Your well-being is important to me."
        ])

    # Check for help requests
    if any(word in message for word in help_requests):
        return random.choice([
            "I'm here to help! I can suggest coping strategies, recommend songs to match your mood, provide wellness routines, or just be someone to talk to. What would be most helpful right now?",
            "I'd be happy to help. I can listen, offer support, suggest self-care activities, or provide information about mental wellness. What kind of support are you looking for?",
            "I'm here to support you. Would you like suggestions for managing stress, improving mood, or enhancing your overall well-being?",
            "I'm ready to assist you. I can offer a listening ear, suggest relaxation techniques, or provide resources for mental wellness. What would you find most helpful?"
        ])

    # Default response for other messages
    return random.choice([
        "Thank you for sharing that with me. How does this affect your day-to-day life?",
        "I appreciate you telling me about this. How are you feeling about it?",
        "That's interesting. Would you like to tell me more about your experience?",
        "I'm here to listen. How can I best support you right now?",
        "Thank you for sharing. What would be most helpful for you in this moment?",
        "I'm here for you. Would you like to explore this topic further?",
        "I value your openness. Is there a specific aspect of this you'd like to focus on?"
    ])

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

