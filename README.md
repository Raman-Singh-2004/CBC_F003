# Mental Health Chatbot

A supportive AI chatbot designed to provide mental health assistance and resources.

## Features

- Simple, user-friendly chat interface
- Dark/light theme toggle
- Emergency mental health resources
- Conversation history saved locally
- Typing indicators for a more natural feel
- Keyboard shortcuts for accessibility
- Multiple AI backend options (Rule-based, Llama, OpenAI)

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mental_health_chatbot.git
   cd mental_health_chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   - Create a file named `.env` in the project root
   - For OpenAI: `OPENAI_API_KEY=your_api_key_here`
   - For HuggingFace: `HUGGINGFACE_API_KEY=your_api_key_here`

### Running the Application

1. Start the HTTP server to serve the frontend:
   ```
   python server.py
   ```

2. In a separate terminal, start one of the Flask backends:
   ```
   # For rule-based responses (no API key needed)
   python app.py

   # For OpenAI GPT-powered responses (requires API key)
   python gpti.py

   # For Llama-powered responses (requires HuggingFace API key)
   python llama_api.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000/index.html
   ```

## Backend Options

### Rule-based (app.py)
- Simple pattern matching for common mental health concerns
- No external API dependencies
- Predefined responses for greetings, feelings, help requests
- Maintains conversation context for better follow-up responses

### OpenAI GPT (gpti.py)
- Integrates with OpenAI's API
- Uses GPT-3.5-turbo model
- Requires an OpenAI API key
- Provides more natural and contextually relevant responses
- Falls back to rule-based responses if API is unavailable

### Llama (llama_api.py)
- Integrates with HuggingFace's Inference API for Llama models
- Uses Meta's Llama-2-7b-chat-hf model
- Requires a HuggingFace API key
- Provides free alternative to OpenAI
- Falls back to rule-based responses if API is unavailable

## Usage

- Type your message in the input field and press Enter or click Send
- Click the moon/sun icon to toggle between dark and light themes
- Click the question mark button to access mental health resources
- Use keyboard shortcuts:
  - `/` to focus the input field
  - `Alt+R` to toggle resources panel
  - `Alt+T` to toggle theme

## Important Note

This chatbot is not a replacement for professional mental health services. If you or someone you know is in crisis, please contact a mental health professional or use one of the emergency resources listed in the application.

## License

MIT
