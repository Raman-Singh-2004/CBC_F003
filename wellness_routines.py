"""
Wellness routines module for suggesting daily routines for mental and physical wellness.
"""

import re
import random
from datetime import datetime

# Patterns to identify wellness routine requests
WELLNESS_ROUTINE_PATTERNS = [
    r"(?:suggest|recommend|give me|share|tell me about) (?:a|some) (?:daily|morning|evening|night|wellness|mental health|physical|healthy) routine",
    r"(?:what|how) (?:should|can|do) i (?:do|practice|incorporate|include) (?:for|to improve|to boost|to enhance) (?:my|) (?:mental health|physical health|wellness|wellbeing|well-being|health)",
    r"(?:help|tips|advice) (?:for|with|on) (?:daily|morning|evening|night|wellness|mental health|physical|healthy) routine",
    r"(?:how|what) (?:to|can i|should i) (?:start|begin|create|establish|develop) (?:a|my) (?:daily|morning|evening|night|wellness|mental health|physical|healthy) routine",
    r"(?:need|want) (?:a|some) (?:daily|morning|evening|night|wellness|mental health|physical|healthy) routine",
    r"(?:improve|boost|enhance|better) (?:my|) (?:mental health|physical health|wellness|wellbeing|well-being|health)",
    r"(?:feeling|been feeling) (?:stressed|anxious|depressed|down|low|sad|tired|exhausted|burnt out|overwhelmed) (?:routine|habits|practices|activities)",
    r"(?:daily|morning|evening|night|wellness|mental health|physical|healthy) (?:routine|habits|practices|activities) (?:for|to) (?:improve|boost|enhance|better) (?:mental health|physical health|wellness|wellbeing|well-being|health)",
    r"(?:what|how) (?:are|about) (?:good|healthy|effective|helpful) (?:daily|morning|evening|night|wellness|mental health|physical|healthy) (?:routine|habits|practices|activities)"
]

# Keywords to identify specific routine types
ROUTINE_TYPE_KEYWORDS = {
    "morning": ["morning", "wake up", "start the day", "early", "sunrise", "breakfast", "am"],
    "evening": ["evening", "night", "before bed", "bedtime", "sleep", "pm", "sunset"],
    "mental": ["mental", "mind", "brain", "cognitive", "emotional", "mood", "stress", "anxiety", "depression", "psychological"],
    "physical": ["physical", "body", "exercise", "workout", "fitness", "strength", "health", "energy", "active"],
    "general": ["wellness", "wellbeing", "well-being", "health", "routine", "daily", "habits", "lifestyle", "practices", "activities"]
}

# Morning wellness routines
MORNING_ROUTINES = [
    {
        "title": "Mindful Morning Routine",
        "description": "A gentle routine to start your day with awareness and positivity.",
        "steps": [
            "Wake up at the same time each day (ideally between 6-7 AM) to regulate your body's internal clock.",
            "Before reaching for your phone, take 3 deep breaths and set a positive intention for the day.",
            "Drink a glass of water with lemon to hydrate and kickstart your metabolism.",
            "Spend 5-10 minutes meditating or practicing mindfulness to center yourself.",
            "Do 5-10 minutes of gentle stretching or yoga to wake up your body.",
            "Take a refreshing shower, alternating between warm and cool water to boost circulation.",
            "Eat a nutritious breakfast with protein, healthy fats, and complex carbohydrates.",
            "Review your priorities for the day and identify your top 3 most important tasks."
        ],
        "benefits": [
            "Reduces morning stress and anxiety",
            "Improves mental clarity and focus",
            "Boosts physical energy levels",
            "Creates a sense of control and purpose",
            "Establishes a positive tone for the day"
        ]
    },
    {
        "title": "Energizing Morning Routine",
        "description": "A dynamic routine to boost your energy and productivity for the day ahead.",
        "steps": [
            "Wake up early (5:30-6:30 AM) and immediately get out of bed without hitting snooze.",
            "Drink 16oz of water to rehydrate after sleep.",
            "Do 15-20 minutes of moderate to high-intensity exercise (jogging, HIIT, or strength training).",
            "Take a cold shower to increase alertness and improve circulation.",
            "Practice 5 minutes of box breathing or another breathing exercise.",
            "Eat a protein-rich breakfast with fruits or vegetables.",
            "Spend 10 minutes journaling or planning your day with specific goals.",
            "Listen to uplifting music or an educational podcast while getting ready."
        ],
        "benefits": [
            "Significantly increases physical energy and mental alertness",
            "Boosts metabolism and supports weight management",
            "Improves mood through endorphin release",
            "Enhances productivity and focus throughout the day",
            "Builds discipline and willpower"
        ]
    },
    {
        "title": "Grounding Morning Routine",
        "description": "A nurturing routine to help you feel centered and connected to yourself.",
        "steps": [
            "Wake up naturally with the sunrise if possible, or use a sunrise alarm clock.",
            "Begin with 5 minutes of gratitude practice, noting 3 things you're thankful for.",
            "Drink warm water with lemon, honey, and a pinch of turmeric or ginger.",
            "Spend 10-15 minutes in meditation, focusing on your breath and body sensations.",
            "Do gentle yoga or tai chi movements for 10-15 minutes.",
            "Take time to prepare and mindfully eat a nourishing breakfast.",
            "Spend a few minutes in nature, even if just sitting by a window or on a balcony.",
            "Set intentions for how you want to feel throughout the day."
        ],
        "benefits": [
            "Reduces anxiety and promotes emotional stability",
            "Creates a sense of connection to yourself and the present moment",
            "Supports digestive health and immune function",
            "Cultivates a positive mindset and resilience",
            "Helps maintain calm energy throughout the day"
        ]
    }
]

# Evening wellness routines
EVENING_ROUTINES = [
    {
        "title": "Relaxing Wind-Down Routine",
        "description": "A calming routine to help you transition from day to night and prepare for restful sleep.",
        "steps": [
            "Set a consistent bedtime and begin your wind-down routine 1-2 hours before.",
            "Turn off electronic devices or use blue light filters to support melatonin production.",
            "Take a warm bath or shower to relax muscles and lower your core temperature.",
            "Practice gentle stretching or restorative yoga poses for 10-15 minutes.",
            "Spend 10 minutes journaling about your day or writing a gratitude list.",
            "Drink calming herbal tea like chamomile, lavender, or valerian root.",
            "Read a physical book (not on a screen) for 15-30 minutes.",
            "Practice 5-10 minutes of meditation or deep breathing exercises in bed."
        ],
        "benefits": [
            "Improves sleep quality and reduces insomnia",
            "Lowers stress hormones like cortisol",
            "Helps process the day's events and emotions",
            "Creates a clear boundary between work/activity and rest",
            "Supports overall mental health and emotional regulation"
        ]
    },
    {
        "title": "Reflective Evening Routine",
        "description": "A thoughtful routine focused on processing your day and preparing for tomorrow.",
        "steps": [
            "Set aside 30-60 minutes before bed for your evening routine.",
            "Review your day's accomplishments and challenges in a journal.",
            "Practice a 'brain dump' by writing down any lingering thoughts or to-dos for tomorrow.",
            "Prepare your environment for tomorrow (lay out clothes, prepare lunch, etc.).",
            "Do a quick 10-minute tidy-up of your living space.",
            "Engage in a calming activity like coloring, knitting, or listening to soft music.",
            "Practice a body scan meditation, relaxing each part of your body systematically.",
            "Use aromatherapy with lavender or chamomile essential oils to signal sleep time."
        ],
        "benefits": [
            "Reduces anxiety about the next day",
            "Provides closure to the current day",
            "Improves sleep quality by clearing mental clutter",
            "Builds self-awareness and emotional intelligence",
            "Creates a sense of control and preparedness"
        ]
    },
    {
        "title": "Digital Detox Evening Routine",
        "description": "A technology-free routine to help reset your nervous system and improve sleep quality.",
        "steps": [
            "Turn off all screens at least 1 hour before bedtime.",
            "Place your phone in another room or in a drawer to avoid temptation.",
            "Dim the lights in your home to signal to your body that it's time to wind down.",
            "Engage in a screen-free activity like reading, drawing, or playing a musical instrument.",
            "Practice a facial massage or skincare routine as a form of self-care.",
            "Write down 3 things that went well today and why they matter to you.",
            "Do gentle stretching focusing on areas that hold tension (neck, shoulders, lower back).",
            "Practice 4-7-8 breathing (inhale for 4, hold for 7, exhale for 8) as you lie in bed."
        ],
        "benefits": [
            "Significantly improves sleep quality and reduces time to fall asleep",
            "Decreases exposure to stimulating content before bed",
            "Reduces eye strain and mental overstimulation",
            "Promotes mindfulness and presence",
            "Helps reset unhealthy technology habits"
        ]
    }
]

# Mental wellness routines
MENTAL_WELLNESS_ROUTINES = [
    {
        "title": "Daily Mental Wellness Routine",
        "description": "A comprehensive routine to support your mental health throughout the day.",
        "steps": [
            "Start your day with 10 minutes of meditation to set a calm tone.",
            "Practice positive affirmations or mantras that counter negative thought patterns.",
            "Take short 5-minute mindfulness breaks every 2-3 hours during your day.",
            "Spend at least 20 minutes outdoors, preferably in a natural setting.",
            "Engage in a creative activity for 15-30 minutes (drawing, writing, music, etc.).",
            "Connect meaningfully with at least one person each day, even if briefly.",
            "Practice gratitude by noting 3 positive experiences at the end of your day.",
            "Set aside 10 minutes for reflection and journaling before bed."
        ],
        "benefits": [
            "Reduces symptoms of anxiety and depression",
            "Improves emotional regulation and resilience",
            "Enhances self-awareness and personal growth",
            "Strengthens social connections and support systems",
            "Builds a positive mindset and cognitive flexibility"
        ]
    },
    {
        "title": "Stress Management Routine",
        "description": "A targeted routine to help manage and reduce stress levels.",
        "steps": [
            "Begin your day with 5 minutes of deep breathing exercises.",
            "Practice progressive muscle relaxation for 10 minutes when feeling tense.",
            "Take regular breaks from work using the 50/10 rule (50 minutes of work, 10 minutes of rest).",
            "Go for a 15-20 minute walk after lunch to clear your mind.",
            "Use stress-tracking in a journal to identify patterns and triggers.",
            "Practice setting boundaries by saying no to at least one non-essential request each day.",
            "Engage in a hobby or activity that brings you joy for at least 30 minutes.",
            "End your day with a 'worry dump' where you write down concerns to address tomorrow."
        ],
        "benefits": [
            "Reduces cortisol levels and physical symptoms of stress",
            "Prevents burnout and chronic stress conditions",
            "Improves work productivity and focus",
            "Enhances ability to respond rather than react to stressors",
            "Builds long-term stress resilience"
        ]
    },
    {
        "title": "Mood-Boosting Routine",
        "description": "A routine designed to elevate your mood and combat feelings of sadness or low energy.",
        "steps": [
            "Start your day with 10-15 minutes of light exposure (natural sunlight if possible).",
            "Do 20-30 minutes of aerobic exercise to release endorphins.",
            "Listen to uplifting music or a positive podcast during your commute or morning activities.",
            "Practice random acts of kindness - do something nice for someone else.",
            "Take a 'pleasure inventory' by spending 5 minutes on something you genuinely enjoy.",
            "Connect with a supportive friend or family member, even just via text or a quick call.",
            "Limit news and social media consumption to specific times and durations.",
            "End your day by noting 3 positive moments, no matter how small."
        ],
        "benefits": [
            "Naturally increases serotonin and dopamine levels",
            "Reduces symptoms of mild to moderate depression",
            "Creates positive momentum through small wins",
            "Strengthens social connections that buffer against low mood",
            "Builds awareness of mood patterns and effective interventions"
        ]
    }
]

# Physical wellness routines
PHYSICAL_WELLNESS_ROUTINES = [
    {
        "title": "Daily Movement Routine",
        "description": "A balanced approach to incorporating physical activity throughout your day.",
        "steps": [
            "Start with 5-10 minutes of morning stretching to wake up your body.",
            "Take movement breaks every hour - stand up, stretch, or walk around for 2-3 minutes.",
            "Go for a 20-30 minute walk during lunch or another break in your day.",
            "Do 15-20 minutes of strength training focusing on major muscle groups (can be bodyweight exercises).",
            "Practice good posture throughout the day, especially if you work at a desk.",
            "Take the stairs instead of elevators when possible.",
            "Do 10 minutes of mobility work in the evening to address tight areas.",
            "End your day with gentle stretching to release tension before sleep."
        ],
        "benefits": [
            "Improves cardiovascular health and circulation",
            "Maintains muscle mass and bone density",
            "Reduces risk of chronic diseases like diabetes and heart disease",
            "Boosts energy levels and reduces fatigue",
            "Supports better sleep quality and stress management"
        ]
    },
    {
        "title": "Energy-Optimizing Routine",
        "description": "A routine focused on maximizing your physical energy and vitality throughout the day.",
        "steps": [
            "Drink 16oz of water immediately upon waking to rehydrate.",
            "Eat a balanced breakfast with protein, healthy fats, and complex carbs within an hour of waking.",
            "Take a 10-minute brisk walk outdoors to increase alertness and vitamin D.",
            "Practice time-restricted eating (e.g., eating within an 8-10 hour window) to optimize metabolism.",
            "Stay hydrated by drinking water regularly throughout the day (aim for 2-3 liters total).",
            "Take a 5-minute breathing break when energy dips instead of reaching for caffeine.",
            "Do a 4-minute Tabata workout (20 seconds intense exercise, 10 seconds rest, repeated 8 times) for an afternoon boost.",
            "Avoid heavy meals within 3 hours of bedtime to improve sleep quality."
        ],
        "benefits": [
            "Stabilizes energy levels throughout the day",
            "Reduces reliance on caffeine and sugar for energy",
            "Improves metabolic health and insulin sensitivity",
            "Enhances cellular energy production",
            "Supports healthy circadian rhythms"
        ]
    },
    {
        "title": "Recovery-Focused Routine",
        "description": "A routine designed to support physical recovery and prevent burnout or injury.",
        "steps": [
            "Start with gentle joint mobility exercises for 5-10 minutes in the morning.",
            "Practice deep breathing for 5 minutes to activate your parasympathetic nervous system.",
            "Use a foam roller or massage ball for 10 minutes on tight muscles.",
            "Take a contrast shower (alternating between warm and cold water) to improve circulation.",
            "Schedule at least 2 full rest days per week from intense exercise.",
            "Practice active recovery like walking, swimming, or gentle yoga on rest days.",
            "Use a sleep tracking app or journal to ensure you're getting 7-9 quality hours.",
            "Try a magnesium-rich evening snack (like a small handful of nuts) to support muscle relaxation."
        ],
        "benefits": [
            "Prevents overtraining syndrome and exercise burnout",
            "Reduces risk of repetitive stress injuries",
            "Improves muscle recovery and growth",
            "Enhances immune function and overall resilience",
            "Supports long-term consistency with physical activity"
        ]
    }
]

# General wellness routines
GENERAL_WELLNESS_ROUTINES = [
    {
        "title": "Balanced Daily Wellness Routine",
        "description": "A holistic routine that addresses multiple dimensions of wellbeing.",
        "steps": [
            "Begin your day with 5 minutes of mindfulness meditation.",
            "Drink a glass of water and eat a nutritious breakfast with protein and fiber.",
            "Spend 20-30 minutes on physical movement that you enjoy.",
            "Take short breaks throughout your workday to stretch and reset your focus.",
            "Eat meals mindfully without screens or distractions when possible.",
            "Spend time outdoors, even just 15 minutes, to connect with nature.",
            "Connect meaningfully with someone you care about.",
            "End your day with a gratitude practice and screen-free wind-down time."
        ],
        "benefits": [
            "Creates balance across physical, mental, and emotional wellbeing",
            "Builds sustainable healthy habits that reinforce each other",
            "Reduces stress while increasing energy and resilience",
            "Supports both immediate wellbeing and long-term health",
            "Adaptable to different lifestyles and needs"
        ]
    },
    {
        "title": "Beginner's Wellness Routine",
        "description": "A simple, approachable routine for those new to wellness practices.",
        "steps": [
            "Start with just one new healthy habit each week rather than changing everything at once.",
            "Drink an extra glass of water at three specific times: morning, midday, and evening.",
            "Take a 10-minute walk daily, ideally outdoors.",
            "Practice 3 minutes of deep breathing when you feel stressed.",
            "Add one extra serving of vegetables or fruits to your daily intake.",
            "Set a consistent bedtime and wake-up time, even on weekends.",
            "Spend 5 minutes each evening reflecting on what went well during your day.",
            "Limit screen time to specific hours and take regular digital breaks."
        ],
        "benefits": [
            "Creates sustainable change through gradual implementation",
            "Builds confidence through achievable goals",
            "Establishes foundational habits that support more advanced practices",
            "Reduces overwhelm while still improving wellbeing",
            "Teaches the process of habit formation"
        ]
    },
    {
        "title": "Work-Life Balance Routine",
        "description": "A routine designed to create healthy boundaries between work and personal life.",
        "steps": [
            "Create a consistent morning routine that's just for you, not for work.",
            "Set clear start and end times for your workday and honor them.",
            "Take a proper lunch break away from your workspace.",
            "Schedule short 5-minute breaks every 90 minutes during work hours.",
            "Create an 'end of workday' ritual (like changing clothes or a short walk).",
            "Have tech-free zones or times in your home where work devices aren't allowed.",
            "Plan at least one enjoyable activity each day that's unrelated to productivity.",
            "Practice saying no to non-essential commitments that drain your energy."
        ],
        "benefits": [
            "Reduces burnout and work-related stress",
            "Improves productivity during work hours",
            "Enhances quality of personal and family time",
            "Creates psychological separation between work and rest",
            "Supports overall life satisfaction and mental health"
        ]
    }
]

# All routines combined for easy access
ALL_ROUTINES = {
    "morning": MORNING_ROUTINES,
    "evening": EVENING_ROUTINES,
    "mental": MENTAL_WELLNESS_ROUTINES,
    "physical": PHYSICAL_WELLNESS_ROUTINES,
    "general": GENERAL_WELLNESS_ROUTINES
}

def detect_wellness_routine_request(text):
    """
    Detect if the text contains a request for wellness routines.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Detection results including matched patterns and routine type
    """
    text = text.lower()
    
    # Check for wellness routine patterns
    matches = []
    for pattern in WELLNESS_ROUTINE_PATTERNS:
        if re.search(pattern, text):
            matches.append(pattern)
    
    if not matches:
        return {"is_routine_request": False}
    
    # Determine the type of routine requested
    routine_type = "general"  # Default to general wellness
    
    # Check for specific routine types
    type_matches = {}
    for type_name, keywords in ROUTINE_TYPE_KEYWORDS.items():
        type_matches[type_name] = sum(1 for keyword in keywords if keyword in text)
    
    # Find the type with the most keyword matches
    if type_matches:
        routine_type = max(type_matches.items(), key=lambda x: x[1])[0]
        # If no specific type has matches, default to general
        if type_matches[routine_type] == 0:
            routine_type = "general"
    
    return {
        "is_routine_request": True,
        "routine_type": routine_type,
        "matches": matches
    }

def get_wellness_routine(routine_type="general"):
    """
    Get a wellness routine based on the requested type.
    
    Args:
        routine_type (str): Type of routine to retrieve (morning, evening, mental, physical, general)
        
    Returns:
        dict: A wellness routine with title, description, steps, and benefits
    """
    # Validate routine type
    if routine_type not in ALL_ROUTINES:
        routine_type = "general"
    
    # Select a random routine from the appropriate category
    routines = ALL_ROUTINES[routine_type]
    return random.choice(routines)

def format_wellness_routine(routine):
    """
    Format the wellness routine into a user-friendly response.
    
    Args:
        routine (dict): Wellness routine data
        
    Returns:
        str: Formatted response with routine details
    """
    if not routine:
        return "I don't have a specific wellness routine to suggest at the moment."
    
    response = f"# {routine['title']}\n\n"
    response += f"{routine['description']}\n\n"
    
    response += "## Daily Steps:\n"
    for i, step in enumerate(routine['steps'], 1):
        response += f"{i}. {step}\n"
    
    response += "\n## Benefits:\n"
    for benefit in routine['benefits']:
        response += f"• {benefit}\n"
    
    response += "\nRemember, the best routine is one you can stick with consistently. Start small by incorporating just 1-2 of these steps, then gradually add more as they become habits. Would you like me to suggest which steps to start with?"
    
    return response

def process_wellness_routine_request(text):
    """
    Process text to detect wellness routine requests and generate a response.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Processing results including detection and response
    """
    routine_info = detect_wellness_routine_request(text)
    
    if not routine_info.get("is_routine_request", False):
        return {"is_routine_request": False}
    
    routine_type = routine_info.get("routine_type", "general")
    routine = get_wellness_routine(routine_type)
    response = format_wellness_routine(routine)
    
    return {
        "is_routine_request": True,
        "routine_type": routine_type,
        "routine": routine,
        "response": response
    }
