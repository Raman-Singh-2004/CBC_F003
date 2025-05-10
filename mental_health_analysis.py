"""
Mental health analysis module for detecting potential mental health concerns
and providing appropriate coping strategies.
"""

import re
import random
from datetime import datetime, timedelta

# Dictionary of mental health indicators and their severity levels
MENTAL_HEALTH_INDICATORS = {
    # Depression indicators
    "depression": {
        "keywords": [
            "depressed", "depression", "sad", "hopeless", "worthless", "empty", 
            "no energy", "tired all the time", "can't sleep", "sleeping too much",
            "no interest", "no motivation", "don't enjoy", "don't care anymore",
            "life is pointless", "no point", "giving up", "end it all"
        ],
        "severity_levels": {
            "low": ["sad", "tired", "no energy", "can't sleep", "sleeping too much"],
            "medium": ["depressed", "depression", "hopeless", "no interest", "no motivation", "don't enjoy"],
            "high": ["worthless", "empty", "life is pointless", "no point", "giving up", "end it all"]
        }
    },
    
    # Anxiety indicators
    "anxiety": {
        "keywords": [
            "anxious", "anxiety", "worried", "panic", "fear", "scared", "nervous",
            "stress", "stressed", "overthinking", "can't relax", "racing thoughts",
            "heart racing", "breathing fast", "sweating", "trembling", "shaking",
            "constant worry", "what if", "something bad"
        ],
        "severity_levels": {
            "low": ["worried", "nervous", "stress", "stressed", "overthinking"],
            "medium": ["anxious", "anxiety", "can't relax", "racing thoughts", "constant worry", "what if"],
            "high": ["panic", "fear", "scared", "heart racing", "breathing fast", "sweating", "trembling", "shaking", "something bad"]
        }
    },
    
    # Anger/frustration indicators
    "anger": {
        "keywords": [
            "angry", "anger", "mad", "frustrated", "irritated", "annoyed", "rage",
            "furious", "hate", "resent", "resentment", "explode", "lash out",
            "break things", "hurt someone", "violent thoughts"
        ],
        "severity_levels": {
            "low": ["annoyed", "irritated", "frustrated"],
            "medium": ["angry", "anger", "mad", "hate", "resent", "resentment"],
            "high": ["rage", "furious", "explode", "lash out", "break things", "hurt someone", "violent thoughts"]
        }
    },
    
    # Self-harm/suicidal indicators
    "self_harm": {
        "keywords": [
            "hurt myself", "harm myself", "cut myself", "cutting", "self-harm", "self harm",
            "suicide", "suicidal", "kill myself", "end my life", "better off dead",
            "no reason to live", "can't go on", "want to die", "don't want to be here"
        ],
        "severity_levels": {
            "low": [],  # No low severity for self-harm indicators
            "medium": ["hurt myself", "harm myself", "self-harm", "self harm"],
            "high": ["cut myself", "cutting", "suicide", "suicidal", "kill myself", "end my life", 
                    "better off dead", "no reason to live", "can't go on", "want to die", "don't want to be here"]
        }
    }
}

# Coping strategies for different mental health concerns
COPING_STRATEGIES = {
    "depression": {
        "low": [
            "Try to get some sunlight and fresh air today, even just for 10 minutes.",
            "Consider reaching out to a friend or family member for a brief chat.",
            "Try to do one small activity that you used to enjoy, even if you don't feel like it.",
            "Practice basic self-care: take a shower, eat a nutritious meal, or get some rest.",
            "Set a very small, achievable goal for today to create a sense of accomplishment."
        ],
        "medium": [
            "Consider establishing a daily routine to provide structure to your day.",
            "Physical activity, even just a short walk, can help boost your mood through endorphin release.",
            "Mindfulness meditation can help you stay present rather than dwelling on negative thoughts.",
            "Try journaling about your feelings to externalize them and gain perspective.",
            "Limit exposure to negative news and social media that might worsen your mood."
        ],
        "high": [
            "Please consider speaking with a mental health professional who can provide proper support.",
            "If you have a therapist or counselor, now would be a good time to schedule a session.",
            "Remember that depression often lies to us about our worth and future prospects.",
            "Try to be as gentle with yourself as you would be with a good friend going through this.",
            "Focus just on getting through today - sometimes taking things one day at a time helps."
        ]
    },
    
    "anxiety": {
        "low": [
            "Try a brief breathing exercise: breathe in for 4 counts, hold for 2, exhale for 6.",
            "Ground yourself by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
            "Take a short break from what you're doing to stretch or move around.",
            "Consider limiting caffeine which can sometimes worsen anxiety symptoms.",
            "Write down your worries to get them out of your head and onto paper."
        ],
        "medium": [
            "Progressive muscle relaxation can help reduce physical tension - try tensing and releasing each muscle group.",
            "Challenge anxious thoughts by asking: What's the evidence? Is there another way to look at this? What would I tell a friend?",
            "Distract yourself with an engaging activity that requires focus, like a puzzle or craft.",
            "Try the 5-4-3-2-1 grounding technique to bring yourself back to the present moment.",
            "Limit exposure to triggers that you know increase your anxiety when possible."
        ],
        "high": [
            "If you're experiencing a panic attack, remember it will pass. Focus on your breathing and remind yourself you're safe.",
            "Consider speaking with a mental health professional who can provide strategies specific to your situation.",
            "Try to accept the anxiety rather than fighting it - sometimes resistance makes it stronger.",
            "Engage your body to release tension: try running in place, doing jumping jacks, or even screaming into a pillow.",
            "Remember that your anxious thoughts are not facts, even though they feel very real."
        ]
    },
    
    "anger": {
        "low": [
            "Take a brief time-out from the situation to collect your thoughts.",
            "Try counting to 10 slowly before responding to give your initial reaction time to pass.",
            "Take a few deep breaths to help calm your physiological response.",
            "Ask yourself if this will matter in a day, a week, or a month from now.",
            "Try changing your environment briefly - step outside or into another room."
        ],
        "medium": [
            "Physical activity can help release tension - try going for a brisk walk or run.",
            "Express your feelings calmly using 'I' statements rather than accusatory language.",
            "Look for the underlying emotion beneath the anger - often it's hurt, fear, or frustration.",
            "Try journaling about what's making you angry to gain clarity and perspective.",
            "Practice relaxation techniques like deep breathing or progressive muscle relaxation."
        ],
        "high": [
            "Remove yourself from the situation until you feel calmer to prevent saying or doing something you'll regret.",
            "Channel the energy into a physical but safe activity like exercising or punching a pillow.",
            "Consider speaking with a mental health professional about healthy anger management strategies.",
            "Remember that while your feelings are valid, you are in control of your actions.",
            "Try to identify your anger triggers so you can prepare better for them in the future."
        ]
    },
    
    "self_harm": {
        "medium": [
            "Try holding ice cubes in your hands or placing them on your skin where you feel the urge to harm.",
            "Draw on yourself with a red marker where you feel like hurting yourself.",
            "Engage in intense exercise to release endorphins and physical tension.",
            "Call or text a friend or family member you trust.",
            "Distract yourself with an absorbing activity that requires focus and both hands."
        ],
        "high": [
            "Please reach out to a crisis helpline where trained professionals can provide immediate support.",
            "If you have a safety plan, now is the time to use it.",
            "Remove any items you might use to harm yourself if you can do so safely.",
            "If you have a therapist or counselor, contact them right away.",
            "Remember that these intense feelings will pass, even though it doesn't feel like it right now."
        ]
    }
}

# Crisis resources information
CRISIS_RESOURCES = {
    "US": {
        "National Suicide Prevention Lifeline": "1-800-273-8255",
        "Crisis Text Line": "Text HOME to 741741",
        "SAMHSA's National Helpline": "1-800-662-HELP (4357)"
    },
    "International": {
        "International Association for Suicide Prevention": "https://www.iasp.info/resources/Crisis_Centres/",
        "Befrienders Worldwide": "https://www.befrienders.org/"
    }
}

# User mental health tracking
user_mental_health_history = {}

def analyze_text(text, user_id):
    """
    Analyze text for mental health indicators and track changes over time.
    
    Args:
        text (str): The user's message text
        user_id (str): Unique identifier for the user
        
    Returns:
        dict: Analysis results including concerns, severity, and coping strategies
    """
    text = text.lower()
    
    # Initialize or get user history
    if user_id not in user_mental_health_history:
        user_mental_health_history[user_id] = {
            "messages": [],
            "concerns": {
                "depression": {"count": 0, "severity": "none", "first_detected": None, "last_detected": None},
                "anxiety": {"count": 0, "severity": "none", "first_detected": None, "last_detected": None},
                "anger": {"count": 0, "severity": "none", "first_detected": None, "last_detected": None},
                "self_harm": {"count": 0, "severity": "none", "first_detected": None, "last_detected": None}
            },
            "last_strategy_provided": {
                "depression": None,
                "anxiety": None,
                "anger": None,
                "self_harm": None
            }
        }
    
    # Add message to history
    user_mental_health_history[user_id]["messages"].append({
        "text": text,
        "timestamp": datetime.now().isoformat()
    })
    
    # Limit history to last 20 messages
    if len(user_mental_health_history[user_id]["messages"]) > 20:
        user_mental_health_history[user_id]["messages"] = user_mental_health_history[user_id]["messages"][-20:]
    
    # Detect concerns and their severity
    detected_concerns = {}
    
    for concern, data in MENTAL_HEALTH_INDICATORS.items():
        # Check for keywords
        found_keywords = [keyword for keyword in data["keywords"] if keyword in text or re.search(r'\b' + re.escape(keyword) + r'\b', text)]
        
        if found_keywords:
            # Determine severity
            severity = "low"
            for level in ["high", "medium", "low"]:
                if any(keyword in found_keywords for keyword in data["severity_levels"].get(level, [])):
                    severity = level
                    break
            
            # Update user history
            user_mental_health_history[user_id]["concerns"][concern]["count"] += 1
            user_mental_health_history[user_id]["concerns"][concern]["severity"] = severity
            user_mental_health_history[user_id]["concerns"][concern]["last_detected"] = datetime.now().isoformat()
            
            if not user_mental_health_history[user_id]["concerns"][concern]["first_detected"]:
                user_mental_health_history[user_id]["concerns"][concern]["first_detected"] = datetime.now().isoformat()
            
            # Add to detected concerns
            detected_concerns[concern] = {
                "severity": severity,
                "keywords": found_keywords
            }
    
    # Prepare response with coping strategies
    response = {
        "detected_concerns": detected_concerns,
        "coping_strategies": {},
        "crisis_resources": None
    }
    
    # Add coping strategies for detected concerns
    for concern, data in detected_concerns.items():
        severity = data["severity"]
        
        # Only provide strategies if we haven't recently provided them for this concern
        last_provided = user_mental_health_history[user_id]["last_strategy_provided"][concern]
        should_provide = True
        
        if last_provided:
            last_time = datetime.fromisoformat(last_provided)
            # Don't provide strategies for the same concern more than once per hour
            if datetime.now() - last_time < timedelta(hours=1):
                should_provide = False
        
        if should_provide and severity in COPING_STRATEGIES.get(concern, {}):
            # Get strategies for this concern and severity
            strategies = COPING_STRATEGIES[concern][severity]
            # Select a random strategy
            selected_strategy = random.choice(strategies)
            response["coping_strategies"][concern] = selected_strategy
            
            # Update last provided timestamp
            user_mental_health_history[user_id]["last_strategy_provided"][concern] = datetime.now().isoformat()
    
    # Add crisis resources for high severity concerns
    high_severity_concerns = [concern for concern, data in detected_concerns.items() 
                             if data["severity"] == "high"]
    
    if "self_harm" in detected_concerns or high_severity_concerns:
        response["crisis_resources"] = CRISIS_RESOURCES
    
    return response

def get_mental_health_trend(user_id):
    """
    Analyze the user's mental health trend over time.
    
    Args:
        user_id (str): Unique identifier for the user
        
    Returns:
        dict: Trend analysis for each concern
    """
    if user_id not in user_mental_health_history:
        return {"trend": "insufficient_data"}
    
    user_data = user_mental_health_history[user_id]
    
    # Need at least 5 messages for trend analysis
    if len(user_data["messages"]) < 5:
        return {"trend": "insufficient_data"}
    
    trends = {}
    
    for concern, data in user_data["concerns"].items():
        if data["count"] == 0:
            trends[concern] = "not_detected"
            continue
        
        # Check if concern was detected in recent messages
        recent_messages = user_data["messages"][-3:]
        recent_text = " ".join([msg["text"] for msg in recent_messages])
        
        concern_keywords = MENTAL_HEALTH_INDICATORS[concern]["keywords"]
        recent_mentions = sum(1 for keyword in concern_keywords if keyword in recent_text.lower())
        
        if recent_mentions > 0:
            if data["severity"] == "high":
                trends[concern] = "active_high"
            elif data["severity"] == "medium":
                trends[concern] = "active_medium"
            else:
                trends[concern] = "active_low"
        else:
            # Concern was detected before but not in recent messages
            trends[concern] = "improving"
    
    return {"trend": trends}

def format_analysis_response(analysis_result, trend_result=None):
    """
    Format the analysis results into a user-friendly response.
    
    Args:
        analysis_result (dict): Results from analyze_text
        trend_result (dict, optional): Results from get_mental_health_trend
        
    Returns:
        str: Formatted response with concerns and coping strategies
    """
    response = ""
    
    # Add detected concerns
    detected_concerns = analysis_result.get("detected_concerns", {})
    
    if not detected_concerns:
        return None  # No concerns detected
    
    # Add coping strategies
    coping_strategies = analysis_result.get("coping_strategies", {})
    
    if coping_strategies:
        response += "I notice you might be experiencing some challenges. Here's a suggestion that might help:\n\n"
        
        for concern, strategy in coping_strategies.items():
            response += f"• {strategy}\n\n"
    
    # Add crisis resources for high severity concerns
    crisis_resources = analysis_result.get("crisis_resources")
    
    if crisis_resources and "self_harm" in detected_concerns:
        response += "If you're having thoughts of harming yourself, please consider reaching out to one of these resources:\n\n"
        response += f"• National Suicide Prevention Lifeline: {crisis_resources['US']['National Suicide Prevention Lifeline']}\n"
        response += f"• Crisis Text Line: {crisis_resources['US']['Crisis Text Line']}\n\n"
    
    # Add trend information if available
    if trend_result and trend_result.get("trend") != "insufficient_data":
        trends = trend_result.get("trend", {})
        improving_concerns = [concern for concern, status in trends.items() if status == "improving"]
        
        if improving_concerns:
            response += "I've noticed you seem to be doing better with "
            response += ", ".join(improving_concerns).replace("_", " ")
            response += ". That's great progress!\n\n"
    
    return response.strip() if response else None
