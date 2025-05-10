"""
Positive responses module for detecting happy moods and providing
enthusiastic, celebratory responses to reinforce positive emotions.
"""

import re
import random
from datetime import datetime

# Patterns to identify positive moods
POSITIVE_MOOD_PATTERNS = [
    r"i(?:'m| am) (?:feeling )?happy",
    r"i feel (?:so |really |very |extremely )?happy",
    r"i(?:'m| am) (?:feeling )?good",
    r"i feel (?:so |really |very |extremely )?good",
    r"i(?:'m| am) (?:feeling )?great",
    r"i feel (?:so |really |very |extremely )?great",
    r"i(?:'m| am) (?:feeling )?positive",
    r"i feel (?:so |really |very |extremely )?positive",
    r"i(?:'m| am) (?:feeling )?wonderful",
    r"i feel (?:so |really |very |extremely )?wonderful",
    r"i(?:'m| am) (?:feeling )?fantastic",
    r"i feel (?:so |really |very |extremely )?fantastic",
    r"i(?:'m| am) (?:feeling )?excellent",
    r"i feel (?:so |really |very |extremely )?excellent",
    r"i(?:'m| am) (?:feeling )?amazing",
    r"i feel (?:so |really |very |extremely )?amazing",
    r"i(?:'m| am) (?:feeling )?joyful",
    r"i feel (?:so |really |very |extremely )?joyful",
    r"i(?:'m| am) (?:feeling )?cheerful",
    r"i feel (?:so |really |very |extremely )?cheerful",
    r"i(?:'m| am) (?:feeling )?delighted",
    r"i feel (?:so |really |very |extremely )?delighted",
    r"i(?:'m| am) (?:feeling )?excited",
    r"i feel (?:so |really |very |extremely )?excited",
    r"i(?:'m| am) (?:feeling )?thrilled",
    r"i feel (?:so |really |very |extremely )?thrilled",
    r"i(?:'m| am) (?:feeling )?ecstatic",
    r"i feel (?:so |really |very |extremely )?ecstatic",
    r"i(?:'m| am) (?:feeling )?content",
    r"i feel (?:so |really |very |extremely )?content",
    r"i(?:'m| am) (?:feeling )?satisfied",
    r"i feel (?:so |really |very |extremely )?satisfied",
    r"i(?:'m| am) (?:feeling )?pleased",
    r"i feel (?:so |really |very |extremely )?pleased",
    r"i(?:'m| am) (?:feeling )?grateful",
    r"i feel (?:so |really |very |extremely )?grateful",
    r"i(?:'m| am) (?:feeling )?thankful",
    r"i feel (?:so |really |very |extremely )?thankful",
    r"i(?:'m| am) (?:feeling )?blessed",
    r"i feel (?:so |really |very |extremely )?blessed",
    r"i(?:'m| am) (?:feeling )?optimistic",
    r"i feel (?:so |really |very |extremely )?optimistic",
    r"i(?:'m| am) (?:feeling )?hopeful",
    r"i feel (?:so |really |very |extremely )?hopeful",
    r"i(?:'m| am) (?:feeling )?confident",
    r"i feel (?:so |really |very |extremely )?confident",
    r"i(?:'m| am) (?:feeling )?proud",
    r"i feel (?:so |really |very |extremely )?proud",
    r"i(?:'m| am) (?:feeling )?accomplished",
    r"i feel (?:so |really |very |extremely )?accomplished",
    r"i(?:'m| am) (?:feeling )?successful",
    r"i feel (?:so |really |very |extremely )?successful",
    r"i(?:'m| am) (?:feeling )?fulfilled",
    r"i feel (?:so |really |very |extremely )?fulfilled",
    r"i(?:'m| am) (?:feeling )?peaceful",
    r"i feel (?:so |really |very |extremely )?peaceful",
    r"i(?:'m| am) (?:feeling )?calm",
    r"i feel (?:so |really |very |extremely )?calm",
    r"i(?:'m| am) (?:feeling )?relaxed",
    r"i feel (?:so |really |very |extremely )?relaxed",
    r"i(?:'m| am) (?:feeling )?serene",
    r"i feel (?:so |really |very |extremely )?serene",
    r"i(?:'m| am) (?:feeling )?tranquil",
    r"i feel (?:so |really |very |extremely )?tranquil",
    r"i(?:'m| am) (?:feeling )?at peace",
    r"i feel (?:so |really |very |extremely )?at peace",
    r"i(?:'m| am) (?:feeling )?at ease",
    r"i feel (?:so |really |very |extremely )?at ease",
    r"i(?:'m| am) (?:feeling )?balanced",
    r"i feel (?:so |really |very |extremely )?balanced",
    r"i(?:'m| am) (?:feeling )?centered",
    r"i feel (?:so |really |very |extremely )?centered",
    r"i(?:'m| am) (?:feeling )?grounded",
    r"i feel (?:so |really |very |extremely )?grounded",
    r"i(?:'m| am) (?:feeling )?energized",
    r"i feel (?:so |really |very |extremely )?energized",
    r"i(?:'m| am) (?:feeling )?motivated",
    r"i feel (?:so |really |very |extremely )?motivated",
    r"i(?:'m| am) (?:feeling )?inspired",
    r"i feel (?:so |really |very |extremely )?inspired",
    r"i(?:'m| am) (?:feeling )?creative",
    r"i feel (?:so |really |very |extremely )?creative",
    r"i(?:'m| am) (?:feeling )?productive",
    r"i feel (?:so |really |very |extremely )?productive",
    r"i(?:'m| am) (?:feeling )?focused",
    r"i feel (?:so |really |very |extremely )?focused",
    r"i(?:'m| am) (?:feeling )?determined",
    r"i feel (?:so |really |very |extremely )?determined",
    r"i(?:'m| am) (?:feeling )?resolute",
    r"i feel (?:so |really |very |extremely )?resolute",
    r"i(?:'m| am) (?:feeling )?strong",
    r"i feel (?:so |really |very |extremely )?strong",
    r"i(?:'m| am) (?:feeling )?powerful",
    r"i feel (?:so |really |very |extremely )?powerful",
    r"i(?:'m| am) (?:feeling )?capable",
    r"i feel (?:so |really |very |extremely )?capable",
    r"i(?:'m| am) (?:feeling )?competent",
    r"i feel (?:so |really |very |extremely )?competent",
    r"i(?:'m| am) (?:feeling )?skilled",
    r"i feel (?:so |really |very |extremely )?skilled",
    r"i(?:'m| am) (?:feeling )?talented",
    r"i feel (?:so |really |very |extremely )?talented",
    r"i(?:'m| am) (?:feeling )?gifted",
    r"i feel (?:so |really |very |extremely )?gifted",
    r"i(?:'m| am) (?:feeling )?special",
    r"i feel (?:so |really |very |extremely )?special",
    r"i(?:'m| am) (?:feeling )?unique",
    r"i feel (?:so |really |very |extremely )?unique",
    r"i(?:'m| am) (?:feeling )?valued",
    r"i feel (?:so |really |very |extremely )?valued",
    r"i(?:'m| am) (?:feeling )?appreciated",
    r"i feel (?:so |really |very |extremely )?appreciated",
    r"i(?:'m| am) (?:feeling )?loved",
    r"i feel (?:so |really |very |extremely )?loved",
    r"i(?:'m| am) (?:feeling )?cherished",
    r"i feel (?:so |really |very |extremely )?cherished",
    r"i(?:'m| am) (?:feeling )?adored",
    r"i feel (?:so |really |very |extremely )?adored",
    r"i(?:'m| am) (?:feeling )?cared for",
    r"i feel (?:so |really |very |extremely )?cared for",
    r"i(?:'m| am) (?:feeling )?supported",
    r"i feel (?:so |really |very |extremely )?supported",
    r"i(?:'m| am) (?:feeling )?encouraged",
    r"i feel (?:so |really |very |extremely )?encouraged",
    r"i(?:'m| am) (?:feeling )?uplifted",
    r"i feel (?:so |really |very |extremely )?uplifted",
    r"i(?:'m| am) (?:feeling )?elevated",
    r"i feel (?:so |really |very |extremely )?elevated",
    r"i(?:'m| am) (?:feeling )?high",
    r"i feel (?:so |really |very |extremely )?high",
    r"i(?:'m| am) (?:feeling )?on top of the world",
    r"i feel (?:so |really |very |extremely )?on top of the world",
    r"i(?:'m| am) (?:feeling )?on cloud nine",
    r"i feel (?:so |really |very |extremely )?on cloud nine",
    r"i(?:'m| am) (?:feeling )?over the moon",
    r"i feel (?:so |really |very |extremely )?over the moon",
    r"i(?:'m| am) (?:feeling )?in seventh heaven",
    r"i feel (?:so |really |very |extremely )?in seventh heaven",
    r"i(?:'m| am) (?:feeling )?in high spirits",
    r"i feel (?:so |really |very |extremely )?in high spirits",
    r"i(?:'m| am) (?:feeling )?in a good mood",
    r"i feel (?:so |really |very |extremely )?in a good mood",
    r"i(?:'m| am) (?:feeling )?in a great mood",
    r"i feel (?:so |really |very |extremely )?in a great mood",
    r"i(?:'m| am) (?:feeling )?in a positive mood",
    r"i feel (?:so |really |very |extremely )?in a positive mood",
    r"i(?:'m| am) (?:feeling )?in a wonderful mood",
    r"i feel (?:so |really |very |extremely )?in a wonderful mood",
    r"i(?:'m| am) (?:feeling )?in a fantastic mood",
    r"i feel (?:so |really |very |extremely )?in a fantastic mood",
    r"i(?:'m| am) (?:feeling )?in an excellent mood",
    r"i feel (?:so |really |very |extremely )?in an excellent mood",
    r"i(?:'m| am) (?:feeling )?in an amazing mood",
    r"i feel (?:so |really |very |extremely )?in an amazing mood",
    r"i(?:'m| am) (?:feeling )?in a joyful mood",
    r"i feel (?:so |really |very |extremely )?in a joyful mood",
    r"i(?:'m| am) (?:feeling )?in a cheerful mood",
    r"i feel (?:so |really |very |extremely )?in a cheerful mood",
    r"i(?:'m| am) (?:feeling )?in a delighted mood",
    r"i feel (?:so |really |very |extremely )?in a delighted mood",
    r"today is a good day",
    r"today is a great day",
    r"today is a wonderful day",
    r"today is a fantastic day",
    r"today is a beautiful day",
    r"today is a perfect day",
    r"today is a blessed day",
    r"today is a happy day",
    r"today is a joyful day",
    r"today is a cheerful day",
    r"today is a delightful day",
    r"today is an amazing day",
    r"today is an excellent day",
    r"today is a positive day",
    r"today is a productive day",
    r"today is a successful day",
    r"today is a fulfilling day",
    r"today is a peaceful day",
    r"today is a calm day",
    r"today is a relaxing day",
    r"today is a serene day",
    r"today is a tranquil day",
    r"today is a balanced day",
    r"today is a centered day",
    r"today is a grounded day",
    r"today is an energizing day",
    r"today is a motivating day",
    r"today is an inspiring day",
    r"today is a creative day",
    r"today is a focused day"
]

# Enthusiastic responses for positive moods
POSITIVE_RESPONSES = [
    "That's fantastic! 🎉 I'm so happy to hear you're feeling good. Your positive energy is contagious!",
    
    "Wonderful! 🌟 It's so great to hear you're in a positive mood. Those good feelings deserve to be celebrated!",
    
    "That makes me so happy to hear! 😊 Positive emotions are worth savoring - take a moment to really enjoy this feeling.",
    
    "Awesome! 🙌 Your happiness matters, and I'm genuinely glad you're feeling good today.",
    
    "That's terrific news! 💫 Happiness looks good on you - I hope this positive feeling stays with you!",
    
    "I'm thrilled to hear that! 🌈 Positive moments like this are precious - they're like little gifts we give ourselves.",
    
    "How wonderful! 🌻 Your happiness brightens the day. Thanks for sharing your positive feelings!",
    
    "That's music to my ears! 🎵 Feeling good is something to celebrate and share. I'm glad you did!",
    
    "Brilliant! ✨ Positive emotions help us build resilience for challenging times. Enjoy this moment fully!",
    
    "I'm so glad to hear you're feeling positive! 🌞 These moments of joy are what make life beautiful.",
    
    "That's excellent! 🎊 Happiness is a wonderful state to be in. May this feeling stay with you!",
    
    "Fantastic! 🌠 Your positive mood is something to cherish. I hope it continues throughout your day!",
    
    "That's really great to hear! 😄 Positive emotions are worth acknowledging and celebrating.",
    
    "Marvelous! 🎈 I'm genuinely happy that you're feeling good. Your positive energy is a gift!",
    
    "How delightful! 🌷 Happiness is contagious, and I find myself smiling knowing you're in good spirits!",
    
    "That's wonderful news! 🌈 Positive feelings are treasures - I hope you can savor this moment.",
    
    "I'm so pleased to hear that! 🌟 Your happiness matters, and I'm glad you're experiencing these positive emotions.",
    
    "Excellent! 🎉 Feeling good is something to celebrate. I hope this positive energy stays with you!",
    
    "That's just awesome! 😊 Your positive mood brightens not just your day, but those around you too.",
    
    "Brilliant! ✨ I'm genuinely happy to hear you're feeling good. These positive moments are precious!"
]

# Positive affirmations to reinforce good feelings
POSITIVE_AFFIRMATIONS = [
    "You deserve every bit of happiness that comes your way.",
    
    "Your positive attitude creates positive circumstances.",
    
    "The joy you feel today is a reflection of the light within you.",
    
    "When you're happy, you're at your most powerful and authentic.",
    
    "Your positive energy has a ripple effect that touches others around you.",
    
    "Happiness is your natural state - you're simply returning home.",
    
    "The good feelings you experience today help build resilience for tomorrow.",
    
    "Your capacity for joy is unlimited - there's always more happiness available to you.",
    
    "By acknowledging your positive feelings, you're inviting more of them into your life.",
    
    "Your happiness is important and worthy of celebration.",
    
    "The positive energy you cultivate today creates momentum for tomorrow.",
    
    "When you honor your joy, you give others permission to do the same.",
    
    "Your happiness is not just a feeling - it's a powerful force for good in your life.",
    
    "The positive thoughts you think today are creating your reality tomorrow.",
    
    "Your joy is a gift not just to yourself, but to everyone around you.",
    
    "By celebrating your happiness, you're training your mind to notice more things to be happy about.",
    
    "The positive feelings you experience are evidence of your inner strength and resilience.",
    
    "Your capacity for happiness is a superpower - it can transform any situation.",
    
    "The joy you feel is a reminder of how wonderful life can be when we're present for it.",
    
    "Your positive mood is not just luck - it's something you've created through your choices and perspective."
]

def detect_positive_mood(text):
    """
    Detect positive moods in the user's message.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Detection results including matched patterns
    """
    text = text.lower()
    
    # Check for positive mood patterns
    matches = []
    for pattern in POSITIVE_MOOD_PATTERNS:
        if re.search(r'\b' + pattern + r'\b', text):
            matches.append(pattern)
    
    if not matches:
        return {"has_positive_mood": False}
    
    return {
        "has_positive_mood": True,
        "patterns": matches
    }

def generate_positive_response():
    """
    Generate an enthusiastic response and positive affirmation.
    
    Returns:
        dict: Response including enthusiastic message and affirmation
    """
    # Select a random enthusiastic response
    response = random.choice(POSITIVE_RESPONSES)
    
    # Select a random positive affirmation
    affirmation = random.choice(POSITIVE_AFFIRMATIONS)
    
    return {
        "response": response,
        "affirmation": affirmation
    }

def format_positive_response(positive_response_data):
    """
    Format the positive response into a user-friendly message.
    
    Args:
        positive_response_data (dict): Response data
        
    Returns:
        str: Formatted response with enthusiastic message and affirmation
    """
    response = positive_response_data.get("response", "")
    affirmation = positive_response_data.get("affirmation", "")
    
    formatted_response = f"{response}\n\n{affirmation}"
    
    return formatted_response

def process_positive_mood(text):
    """
    Process text to detect positive moods and generate enthusiastic responses.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Processing results including detection and response
    """
    mood_info = detect_positive_mood(text)
    
    if not mood_info.get("has_positive_mood", False):
        return {"has_positive_mood": False}
    
    positive_response = generate_positive_response()
    response = format_positive_response(positive_response)
    
    return {
        "has_positive_mood": True,
        "patterns": mood_info.get("patterns", []),
        "response": response
    }
