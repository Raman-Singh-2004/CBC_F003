"""
Mood encouragement module for detecting negative moods and providing
encouraging quotes and lovable lines to uplift the user.
"""

import re
import random
from datetime import datetime, timedelta

# Patterns to identify negative moods
NEGATIVE_MOOD_PATTERNS = {
    "sadness": [
        r"i(?:'m| am) (?:feeling )?sad",
        r"i feel (?:so |really |very |extremely )?sad",
        r"i(?:'m| am) (?:feeling )?down",
        r"i feel (?:so |really |very |extremely )?down",
        r"i(?:'m| am) (?:feeling )?blue",
        r"i feel (?:so |really |very |extremely )?blue",
        r"i(?:'m| am) (?:feeling )?unhappy",
        r"i feel (?:so |really |very |extremely )?unhappy",
        r"i(?:'m| am) (?:feeling )?miserable",
        r"i feel (?:so |really |very |extremely )?miserable",
        r"i(?:'m| am) (?:feeling )?heartbroken",
        r"i feel (?:so |really |very |extremely )?heartbroken",
        r"i want to cry",
        r"i(?:'ve| have) been crying",
        r"i feel like crying",
        r"i(?:'m| am) tearful",
        r"everything is (?:so |really |very |extremely )?sad",
        r"life is (?:so |really |very |extremely )?sad",
        r"nothing makes me happy",
        r"i can't feel happy",
        r"i don't feel joy",
        r"i(?:'m| am) (?:feeling )?low",
        r"i feel (?:so |really |very |extremely )?low",
        r"i(?:'m| am) (?:feeling )?gloomy",
        r"i feel (?:so |really |very |extremely )?gloomy",
        r"i(?:'m| am) (?:feeling )?melancholy",
        r"i feel (?:so |really |very |extremely )?melancholy",
        r"i(?:'m| am) (?:feeling )?sorrowful",
        r"i feel (?:so |really |very |extremely )?sorrowful",
        r"i(?:'m| am) (?:feeling )?grief",
        r"i feel (?:so |really |very |extremely )?grief",
        r"i(?:'m| am) (?:feeling )?distressed",
        r"i feel (?:so |really |very |extremely )?distressed",
        r"i(?:'m| am) (?:feeling )?disheartened",
        r"i feel (?:so |really |very |extremely )?disheartened",
        r"i(?:'m| am) (?:feeling )?despondent",
        r"i feel (?:so |really |very |extremely )?despondent",
        r"i(?:'m| am) (?:feeling )?dejected",
        r"i feel (?:so |really |very |extremely )?dejected",
        r"i(?:'m| am) (?:feeling )?downcast",
        r"i feel (?:so |really |very |extremely )?downcast",
        r"i(?:'m| am) (?:feeling )?downhearted",
        r"i feel (?:so |really |very |extremely )?downhearted",
        r"i(?:'m| am) (?:feeling )?dismal",
        r"i feel (?:so |really |very |extremely )?dismal",
        r"i(?:'m| am) (?:feeling )?dreary",
        r"i feel (?:so |really |very |extremely )?dreary",
        r"i(?:'m| am) (?:feeling )?weepy",
        r"i feel (?:so |really |very |extremely )?weepy",
        r"i(?:'m| am) (?:feeling )?upset",
        r"i feel (?:so |really |very |extremely )?upset"
    ],
    "depression": [
        r"i(?:'m| am) (?:feeling )?depressed",
        r"i feel (?:so |really |very |extremely )?depressed",
        r"i(?:'m| am) (?:feeling )?hopeless",
        r"i feel (?:so |really |very |extremely )?hopeless",
        r"i(?:'m| am) (?:feeling )?worthless",
        r"i feel (?:so |really |very |extremely )?worthless",
        r"i(?:'m| am) (?:feeling )?empty",
        r"i feel (?:so |really |very |extremely )?empty",
        r"i(?:'m| am) (?:feeling )?numb",
        r"i feel (?:so |really |very |extremely )?numb",
        r"i(?:'m| am) (?:feeling )?nothing",
        r"i feel (?:so |really |very |extremely )?nothing",
        r"i don't care anymore",
        r"i don't see the point",
        r"what's the point",
        r"life is (?:so |really |very |extremely )?meaningless",
        r"i can't see a future",
        r"i have no energy",
        r"i can't get out of bed",
        r"everything feels like a struggle",
        r"i(?:'m| am) struggling to function",
        r"i(?:'m| am) in a dark place",
        r"i(?:'m| am) in a black hole",
        r"i(?:'m| am) at rock bottom",
        r"i(?:'m| am) (?:feeling )?suicidal",
        r"i feel (?:so |really |very |extremely )?suicidal",
        r"i(?:'m| am) (?:feeling )?like ending it all",
        r"i feel (?:so |really |very |extremely )?like ending it all",
        r"i(?:'m| am) (?:feeling )?like giving up",
        r"i feel (?:so |really |very |extremely )?like giving up",
        r"i(?:'m| am) (?:feeling )?like i can't go on",
        r"i feel (?:so |really |very |extremely )?like i can't go on",
        r"i(?:'m| am) (?:feeling )?like i can't take it anymore",
        r"i feel (?:so |really |very |extremely )?like i can't take it anymore",
        r"i(?:'m| am) (?:feeling )?like i'm a burden",
        r"i feel (?:so |really |very |extremely )?like i'm a burden",
        r"i(?:'m| am) (?:feeling )?like i'm worthless",
        r"i feel (?:so |really |very |extremely )?like i'm worthless",
        r"i(?:'m| am) (?:feeling )?like i'm a failure",
        r"i feel (?:so |really |very |extremely )?like i'm a failure",
        r"i(?:'m| am) (?:feeling )?like i'm not good enough",
        r"i feel (?:so |really |very |extremely )?like i'm not good enough",
        r"i(?:'m| am) (?:feeling )?like i'm not worthy",
        r"i feel (?:so |really |very |extremely )?like i'm not worthy",
        r"i(?:'m| am) (?:feeling )?like i'm not deserving",
        r"i feel (?:so |really |very |extremely )?like i'm not deserving",
        r"i(?:'m| am) (?:feeling )?like i'm not lovable",
        r"i feel (?:so |really |very |extremely )?like i'm not lovable"
    ],
    "anxiety": [
        r"i(?:'m| am) (?:feeling )?anxious",
        r"i feel (?:so |really |very |extremely )?anxious",
        r"i(?:'m| am) (?:feeling )?worried",
        r"i feel (?:so |really |very |extremely )?worried",
        r"i(?:'m| am) (?:feeling )?scared",
        r"i feel (?:so |really |very |extremely )?scared",
        r"i(?:'m| am) (?:feeling )?fearful",
        r"i feel (?:so |really |very |extremely )?fearful",
        r"i(?:'m| am) (?:feeling )?nervous",
        r"i feel (?:so |really |very |extremely )?nervous",
        r"i(?:'m| am) (?:feeling )?tense",
        r"i feel (?:so |really |very |extremely )?tense",
        r"i(?:'m| am) (?:feeling )?uneasy",
        r"i feel (?:so |really |very |extremely )?uneasy",
        r"i(?:'m| am) (?:feeling )?apprehensive",
        r"i feel (?:so |really |very |extremely )?apprehensive",
        r"i(?:'m| am) (?:feeling )?restless",
        r"i feel (?:so |really |very |extremely )?restless",
        r"i(?:'m| am) (?:feeling )?jittery",
        r"i feel (?:so |really |very |extremely )?jittery",
        r"i(?:'m| am) (?:feeling )?panicky",
        r"i feel (?:so |really |very |extremely )?panicky",
        r"i(?:'m| am) (?:feeling )?on edge",
        r"i feel (?:so |really |very |extremely )?on edge",
        r"i(?:'m| am) (?:feeling )?stressed",
        r"i feel (?:so |really |very |extremely )?stressed",
        r"i(?:'m| am) (?:feeling )?overwhelmed",
        r"i feel (?:so |really |very |extremely )?overwhelmed",
        r"i(?:'m| am) (?:feeling )?freaking out",
        r"i feel (?:so |really |very |extremely )?freaking out",
        r"i(?:'m| am) (?:feeling )?having a panic attack",
        r"i feel (?:so |really |very |extremely )?having a panic attack",
        r"i(?:'m| am) (?:feeling )?having anxiety",
        r"i feel (?:so |really |very |extremely )?having anxiety",
        r"i(?:'m| am) (?:feeling )?having a panic attack",
        r"i feel (?:so |really |very |extremely )?having a panic attack",
        r"i(?:'m| am) (?:feeling )?having an anxiety attack",
        r"i feel (?:so |really |very |extremely )?having an anxiety attack",
        r"i(?:'m| am) (?:feeling )?having a nervous breakdown",
        r"i feel (?:so |really |very |extremely )?having a nervous breakdown"
    ],
    "loneliness": [
        r"i(?:'m| am) (?:feeling )?lonely",
        r"i feel (?:so |really |very |extremely )?lonely",
        r"i(?:'m| am) (?:feeling )?alone",
        r"i feel (?:so |really |very |extremely )?alone",
        r"i(?:'m| am) (?:feeling )?isolated",
        r"i feel (?:so |really |very |extremely )?isolated",
        r"i(?:'m| am) (?:feeling )?abandoned",
        r"i feel (?:so |really |very |extremely )?abandoned",
        r"i(?:'m| am) (?:feeling )?rejected",
        r"i feel (?:so |really |very |extremely )?rejected",
        r"i(?:'m| am) (?:feeling )?unwanted",
        r"i feel (?:so |really |very |extremely )?unwanted",
        r"i(?:'m| am) (?:feeling )?unloved",
        r"i feel (?:so |really |very |extremely )?unloved",
        r"i(?:'m| am) (?:feeling )?disconnected",
        r"i feel (?:so |really |very |extremely )?disconnected",
        r"i(?:'m| am) (?:feeling )?left out",
        r"i feel (?:so |really |very |extremely )?left out",
        r"i(?:'m| am) (?:feeling )?excluded",
        r"i feel (?:so |really |very |extremely )?excluded",
        r"i(?:'m| am) (?:feeling )?forgotten",
        r"i feel (?:so |really |very |extremely )?forgotten",
        r"i(?:'m| am) (?:feeling )?invisible",
        r"i feel (?:so |really |very |extremely )?invisible",
        r"i(?:'m| am) (?:feeling )?like no one cares",
        r"i feel (?:so |really |very |extremely )?like no one cares",
        r"i(?:'m| am) (?:feeling )?like no one understands",
        r"i feel (?:so |really |very |extremely )?like no one understands",
        r"i(?:'m| am) (?:feeling )?like i have no friends",
        r"i feel (?:so |really |very |extremely )?like i have no friends",
        r"i(?:'m| am) (?:feeling )?like i have no one to talk to",
        r"i feel (?:so |really |very |extremely )?like i have no one to talk to",
        r"i(?:'m| am) (?:feeling )?like i'm all alone",
        r"i feel (?:so |really |very |extremely )?like i'm all alone"
    ],
    "bad_mood": [
        r"i(?:'m| am) (?:feeling )?angry",
        r"i feel (?:so |really |very |extremely )?angry",
        r"i(?:'m| am) (?:feeling )?frustrated",
        r"i feel (?:so |really |very |extremely )?frustrated",
        r"i(?:'m| am) (?:feeling )?irritated",
        r"i feel (?:so |really |very |extremely )?irritated",
        r"i(?:'m| am) (?:feeling )?annoyed",
        r"i feel (?:so |really |very |extremely )?annoyed",
        r"i(?:'m| am) (?:feeling )?upset",
        r"i feel (?:so |really |very |extremely )?upset",
        r"i(?:'m| am) (?:feeling )?tired",
        r"i feel (?:so |really |very |extremely )?tired",
        r"i(?:'m| am) (?:feeling )?exhausted",
        r"i feel (?:so |really |very |extremely )?exhausted",
        r"i(?:'m| am) (?:feeling )?drained",
        r"i feel (?:so |really |very |extremely )?drained",
        r"i(?:'m| am) (?:having|experiencing) a bad day",
        r"i(?:'m| am) (?:having|experiencing) a terrible day",
        r"i(?:'m| am) (?:having|experiencing) a horrible day",
        r"i(?:'m| am) (?:having|experiencing) the worst day",
        r"today is (?:so |really |very |extremely )?bad",
        r"today is (?:so |really |very |extremely )?terrible",
        r"today is (?:so |really |very |extremely )?horrible",
        r"today is the worst",
        r"everything is going wrong",
        r"nothing is going right",
        r"i hate everything",
        r"i hate my life",
        r"i(?:'m| am) (?:feeling )?like a failure",
        r"i feel (?:so |really |very |extremely )?like a failure",
        r"i(?:'m| am) (?:feeling )?useless",
        r"i feel (?:so |really |very |extremely )?useless",
        r"i(?:'m| am) (?:feeling )?inadequate",
        r"i feel (?:so |really |very |extremely )?inadequate",
        r"i(?:'m| am) (?:feeling )?not good enough",
        r"i feel (?:so |really |very |extremely )?not good enough",
        r"i(?:'m| am) (?:feeling )?a disappointment",
        r"i feel (?:so |really |very |extremely )?a disappointment",
        r"i(?:'m| am) (?:feeling )?a burden",
        r"i feel (?:so |really |very |extremely )?a burden"
    ]
}

# Encouraging quotes for different moods
ENCOURAGING_QUOTES = {
    "sadness": [
        "Even the darkest night will end and the sun will rise. — Victor Hugo",
        "The wound is the place where the Light enters you. — Rumi",
        "There are far, far better things ahead than any we leave behind. — C.S. Lewis",
        "Sadness flies away on the wings of time. — Jean de La Fontaine",
        "The way I see it, if you want the rainbow, you gotta put up with the rain. — Dolly Parton",
        "Tears are words that need to be written. — Paulo Coelho",
        "It's okay to not be okay, as long as you are not giving up. — Karen Salmansohn",
        "Sadness is but a wall between two gardens. — Kahlil Gibran",
        "The pain you feel today is the strength you feel tomorrow. — Unknown",
        "Your sadness is a gift. Don't reject it. Don't rush it. Live it fully and use it as fuel to change and grow. — Maxime Lagacé"
    ],
    "depression": [
        "You're not a burden. You're a human with emotions that matter.",
        "Depression is a fog that convinces you it will never lift. But it always does, even when you can't believe it.",
        "Sometimes the bravest thing you can do is simply exist another day when everything feels impossible.",
        "Your story isn't over yet. The world needs the unique gift that only you can give.",
        "Even when you can't see it, there's always a path forward. One tiny step is all you need right now.",
        "The fact that you're still here, still trying, still breathing—that's courage in its purest form.",
        "Depression lies to you about your worth. It's the world's worst narrator of your story.",
        "You've survived 100% of your worst days so far. That's an incredible track record.",
        "Sometimes healing happens so slowly you don't notice it until you look back and see how far you've come.",
        "Your presence in this world matters more than you know. The light you bring is irreplaceable."
    ],
    "bad_mood": [
        "This feeling is temporary. Like clouds passing across the sky, it will move on.",
        "You're allowed to have bad days. They don't define you.",
        "Sometimes the bad days put the good ones into perspective. Both are necessary.",
        "Take a deep breath. You've gotten through every bad day so far—that's a 100% success rate.",
        "It's okay to reset. Tomorrow is a fresh page waiting to be written.",
        "Bad days are just days that are bad, not a bad life.",
        "Your mood is like weather—constantly changing and never permanent.",
        "Even in your worst moments, you're still worthy of kindness—especially from yourself.",
        "This tough moment is shaping you, not defining you.",
        "Sometimes the universe sends rain to clear the path for something beautiful to grow."
    ]
}

# Lovable lines for different moods
LOVABLE_LINES = {
    "sadness": [
        "Your tears are valid, but so is your strength. I see both in you.",
        "Even on your saddest days, you're still worthy of all the love in the world.",
        "The depth of your sadness speaks to the capacity of your heart to feel. That's a beautiful thing.",
        "I wish I could wrap your sadness in comfort until it feels lighter to carry.",
        "Your heart may feel heavy now, but it's still beating with purpose and possibility.",
        "Sadness visits everyone, but it doesn't get to stay forever in a soul as bright as yours.",
        "The universe isn't punishing you—it's preparing you for something that requires the strength you're building now.",
        "Your vulnerability isn't weakness; it's the most authentic form of courage.",
        "I believe in your ability to find joy again, even when that feels impossible right now.",
        "Your sadness matters to me. You matter to me. Always."
    ],
    "depression": [
        "Even when you can't feel your own light, it's still there, and it still matters.",
        "Your existence makes the world better, even on days when you can't feel your own value.",
        "I see you fighting battles that others know nothing about. That quiet courage is remarkable.",
        "Depression tells you you're alone. I'm here to remind you that you're not.",
        "Your worth isn't measured by your productivity or happiness. You are inherently valuable, exactly as you are.",
        "The fact that you're still here, still trying, still reaching out—that's not small. That's everything.",
        "I believe in your tomorrow, even when today feels impossible to bear.",
        "Your depression doesn't make you broken. It makes you human in a world that sometimes forgets we're not machines.",
        "I wish I could show you yourself through my eyes, so you could see the strength I see.",
        "You deserve gentle patience, especially from yourself. Healing isn't linear, and that's okay."
    ],
    "bad_mood": [
        "Your feelings are valid, even the uncomfortable ones. They're all part of your beautiful humanity.",
        "Even on your worst days, you're still worthy of kindness and understanding.",
        "This moment doesn't define you. Your resilience in facing it does.",
        "I see your struggle today, and I still see your light shining through it.",
        "You're allowed to have bad days without it meaning you have a bad life.",
        "Sometimes the bravest thing we can do is simply acknowledge how we feel without judgment.",
        "Your bad day matters to me because you matter to me.",
        "Even when you don't feel strong, I see the strength it takes to keep going.",
        "The fact that you can feel deeply—even the difficult emotions—is a gift, even when it doesn't feel like one.",
        "I believe in your ability to weather this storm, and I'll be here holding space for you until it passes."
    ]
}

# User mood tracking
user_mood_history = {}

def detect_negative_mood(text, user_id):
    """
    Detect negative moods in the user's message.

    Args:
        text (str): The user's message
        user_id (str): Unique identifier for the user

    Returns:
        dict: Detection results including mood type and matched patterns
    """
    text = text.lower()

    # Initialize or get user history
    if user_id not in user_mood_history:
        user_mood_history[user_id] = {
            "moods": [],
            "last_encouragement": {
                "sadness": None,
                "depression": None,
                "bad_mood": None
            }
        }

    # Check for mood patterns
    detected_moods = {}

    for mood_type, patterns in NEGATIVE_MOOD_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                if mood_type not in detected_moods:
                    detected_moods[mood_type] = []
                detected_moods[mood_type].append(pattern)

    if not detected_moods:
        return {"has_negative_mood": False}

    # Update user mood history
    timestamp = datetime.now().isoformat()
    for mood_type in detected_moods:
        user_mood_history[user_id]["moods"].append({
            "type": mood_type,
            "timestamp": timestamp
        })

    # Limit history to last 20 mood entries
    if len(user_mood_history[user_id]["moods"]) > 20:
        user_mood_history[user_id]["moods"] = user_mood_history[user_id]["moods"][-20:]

    return {
        "has_negative_mood": True,
        "mood_types": list(detected_moods.keys()),
        "patterns": detected_moods
    }

def get_encouragement(mood_info, user_id):
    """
    Generate encouraging quotes and lovable lines based on the detected mood.

    Args:
        mood_info (dict): Information about the detected mood
        user_id (str): Unique identifier for the user

    Returns:
        dict: Encouragement including quotes and lovable lines
    """
    if not mood_info.get("has_negative_mood", False):
        return None

    mood_types = mood_info.get("mood_types", [])
    if not mood_types:
        return None

    # Prioritize depression over sadness over bad_mood
    primary_mood = "bad_mood"
    if "sadness" in mood_types:
        primary_mood = "sadness"
    if "depression" in mood_types:
        primary_mood = "depression"

    # Check if we've recently provided encouragement for this mood
    last_encouragement = user_mood_history[user_id]["last_encouragement"].get(primary_mood)
    should_provide = True

    if last_encouragement:
        last_time = datetime.fromisoformat(last_encouragement)
        # Don't provide encouragement for the same mood more than once per hour
        if datetime.now() - last_time < timedelta(hours=1):
            should_provide = False

    if not should_provide:
        return None

    # Select a random quote and lovable line
    quote = random.choice(ENCOURAGING_QUOTES.get(primary_mood, []))
    lovable_line = random.choice(LOVABLE_LINES.get(primary_mood, []))

    # Update last encouragement timestamp
    user_mood_history[user_id]["last_encouragement"][primary_mood] = datetime.now().isoformat()

    return {
        "mood_type": primary_mood,
        "quote": quote,
        "lovable_line": lovable_line
    }

def format_encouragement_response(encouragement):
    """
    Format the encouragement into a user-friendly response.

    Args:
        encouragement (dict): Encouragement data

    Returns:
        str: Formatted response with quote and lovable line
    """
    if not encouragement:
        return None

    mood_type = encouragement.get("mood_type", "")
    quote = encouragement.get("quote", "")
    lovable_line = encouragement.get("lovable_line", "")

    response = "I notice you might be feeling down. Here's something that might help:\n\n"

    if quote:
        response += f"\"{quote}\"\n\n"

    if lovable_line:
        response += f"{lovable_line}\n\n"

    response += "Remember, it's okay to not be okay sometimes. Your feelings are valid, and you're not alone in them."

    return response

def process_mood(text, user_id):
    """
    Process text to detect negative moods and generate encouragement.

    Args:
        text (str): The user's message
        user_id (str): Unique identifier for the user

    Returns:
        dict: Processing results including detection and encouragement
    """
    mood_info = detect_negative_mood(text, user_id)

    if not mood_info.get("has_negative_mood", False):
        return {"has_negative_mood": False}

    encouragement = get_encouragement(mood_info, user_id)
    response = format_encouragement_response(encouragement)

    return {
        "has_negative_mood": True,
        "mood_types": mood_info.get("mood_types", []),
        "encouragement": encouragement,
        "response": response
    }
