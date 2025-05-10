"""
Deep listening module for detecting personal stories, deep thoughts, and past experiences,
and providing positive, encouraging responses.
"""

import re
import random
from datetime import datetime

# Patterns to identify deep thoughts or personal stories
DEEP_THOUGHT_PATTERNS = [
    r"i (?:used to|would) (\w+)",
    r"when i was (\w+)",
    r"in my past",
    r"growing up",
    r"my childhood",
    r"i remember when",
    r"i've been thinking about",
    r"i've realized",
    r"i feel like",
    r"i've been feeling",
    r"i've been struggling with",
    r"i'm trying to",
    r"i want to become",
    r"my goal is",
    r"my dream is",
    r"i wish i could",
    r"i regret",
    r"i miss",
    r"i lost",
    r"i'm afraid",
    r"i'm worried",
    r"i'm scared",
    r"i'm concerned",
    r"i'm proud",
    r"i'm grateful",
    r"i'm thankful",
    r"i appreciate",
    r"i learned",
    r"i discovered",
    r"i realized",
    r"i understand now",
    r"i've changed",
    r"i've grown",
    r"i've improved",
    r"i've overcome",
    r"i've been through",
    r"i experienced",
    r"i went through",
    r"i survived",
    r"i accomplished",
    r"i achieved",
    r"i failed",
    r"i made a mistake",
    r"i hurt someone",
    r"someone hurt me",
    r"i was hurt",
    r"i was abused",
    r"i was bullied",
    r"i was rejected",
    r"i was abandoned",
    r"i was alone",
    r"i felt alone",
    r"i feel alone",
    r"i'm lonely",
    r"i'm isolated",
    r"i'm different",
    r"i don't fit in",
    r"i don't belong",
    r"i'm not good enough",
    r"i'm not worthy",
    r"i'm not deserving",
    r"i'm not lovable",
    r"i'm not capable",
    r"i'm not strong enough",
    r"i'm not smart enough",
    r"i'm not talented enough",
    r"i'm not experienced enough",
    r"i'm not qualified enough",
    r"i'm not confident enough",
    r"i'm not brave enough",
    r"i'm not resilient enough",
    r"i'm not patient enough",
    r"i'm not disciplined enough",
    r"i'm not motivated enough",
    r"i'm not inspired enough",
    r"i'm not creative enough",
    r"i'm not innovative enough",
    r"i'm not original enough",
    r"i'm not unique enough",
    r"i'm not special enough",
    r"i'm not important enough",
    r"i'm not significant enough",
    r"i'm not valuable enough",
    r"i'm not useful enough",
    r"i'm not helpful enough",
    r"i'm not kind enough",
    r"i'm not compassionate enough",
    r"i'm not empathetic enough",
    r"i'm not understanding enough",
    r"i'm not forgiving enough",
    r"i'm not accepting enough",
    r"i'm not tolerant enough",
    r"i'm not patient enough",
    r"i'm not calm enough",
    r"i'm not peaceful enough",
    r"i'm not happy enough",
    r"i'm not joyful enough",
    r"i'm not content enough",
    r"i'm not satisfied enough",
    r"i'm not fulfilled enough",
    r"i'm not complete enough",
    r"i'm not whole enough",
    r"i'm not healed enough",
    r"i'm not recovered enough",
    r"i'm not restored enough",
    r"i'm not renewed enough",
    r"i'm not transformed enough",
    r"i'm not changed enough",
    r"i'm not improved enough",
    r"i'm not better enough",
    r"i'm not good enough",
    r"i'm not perfect enough"
]

# Categories of deep thoughts for more targeted responses
THOUGHT_CATEGORIES = {
    "past_experiences": [
        "used to", "would", "when i was", "in my past", "growing up", "childhood", 
        "remember when", "experienced", "went through", "survived", "been through"
    ],
    "self_reflection": [
        "realized", "thinking about", "understand now", "learned", "discovered", 
        "changed", "grown", "improved", "overcome"
    ],
    "aspirations": [
        "want to become", "goal is", "dream is", "wish i could", "trying to"
    ],
    "regrets": [
        "regret", "miss", "lost", "made a mistake", "hurt someone", "failed"
    ],
    "fears": [
        "afraid", "worried", "scared", "concerned"
    ],
    "gratitude": [
        "proud", "grateful", "thankful", "appreciate", "accomplished", "achieved"
    ],
    "trauma": [
        "hurt", "abused", "bullied", "rejected", "abandoned"
    ],
    "loneliness": [
        "alone", "lonely", "isolated", "different", "don't fit in", "don't belong"
    ],
    "self_doubt": [
        "not good enough", "not worthy", "not deserving", "not lovable", "not capable",
        "not strong enough", "not smart enough", "not talented enough"
    ]
}

# Encouraging responses for different categories
ENCOURAGING_RESPONSES = {
    "past_experiences": [
        "Thank you for sharing that experience with me. Our past shapes us, but it doesn't define our future.",
        "I appreciate you opening up about your past. Those experiences have contributed to the person you are today.",
        "It takes courage to reflect on our past experiences. Thank you for trusting me with yours.",
        "Our history is a powerful teacher. The experiences you've shared show how much you've been through.",
        "Life's journey is filled with many chapters. Thank you for sharing a glimpse of yours with me."
    ],
    "self_reflection": [
        "That's a powerful realization. Self-reflection is a sign of emotional intelligence and growth.",
        "I admire your ability to look inward and gain these insights about yourself.",
        "These moments of clarity can be transformative. I'm glad you're having this realization.",
        "Self-awareness is the first step toward positive change. You're on a good path.",
        "That's a thoughtful observation about yourself. This kind of reflection leads to personal growth."
    ],
    "aspirations": [
        "That's a beautiful goal. I believe you have what it takes to achieve it.",
        "Dreams give us direction and purpose. Yours sounds meaningful and worth pursuing.",
        "I admire your ambition. Taking steps toward your dreams, no matter how small, is progress.",
        "That's an inspiring vision for your future. Keep nurturing that dream.",
        "Goals give our lives meaning. I'm glad you're thinking about what you want for your future."
    ],
    "regrets": [
        "It takes strength to acknowledge regrets. Remember that everyone makes mistakes—they're how we learn and grow.",
        "I hear the regret in your words. Please be gentle with yourself; we all have things we wish we'd done differently.",
        "That sounds difficult to carry. Remember that regret can be a teacher, not just a burden.",
        "Missing someone or something shows the depth of your capacity to care and connect.",
        "I'm sorry for your loss. The pain of losing something or someone important is a reflection of how much it mattered to you."
    ],
    "fears": [
        "It's completely natural to feel afraid. Fear often shows us what matters most to us.",
        "Thank you for sharing your concerns. Acknowledging our fears is often the first step in addressing them.",
        "Your worries are valid. Sometimes naming our fears helps us see them more clearly.",
        "I hear your concerns. Remember that courage isn't the absence of fear, but moving forward despite it.",
        "It's okay to be scared. Many of life's most worthwhile experiences come with a degree of fear."
    ],
    "gratitude": [
        "That's wonderful! Recognizing and appreciating the positive aspects of life is so important.",
        "I'm happy to hear about your accomplishment. You deserve to feel proud of what you've achieved.",
        "Gratitude is a powerful practice. It's great that you're acknowledging these positive elements in your life.",
        "That's definitely something to be proud of. Celebrating our achievements helps us build confidence.",
        "I appreciate you sharing this positive reflection. It's important to recognize our successes along the way."
    ],
    "trauma": [
        "I'm truly sorry you went through that. Your resilience in sharing this shows incredible strength.",
        "That must have been incredibly difficult. Please know that what happened wasn't your fault.",
        "Thank you for trusting me with something so painful. Your willingness to speak about it shows courage.",
        "I can only imagine how challenging that experience was. Your strength in surviving it is remarkable.",
        "That kind of experience can leave deep marks. Your ability to talk about it is a sign of your inner strength."
    ],
    "loneliness": [
        "Feeling disconnected from others can be really painful. Your feelings are completely valid.",
        "I'm sorry you're feeling isolated. Remember that many people feel this way at times, even when it seems like they don't.",
        "Feeling like you don't belong is a difficult experience. Please know that you have inherent worth and value.",
        "Loneliness can be so challenging. Your openness about these feelings shows self-awareness and courage.",
        "I hear how isolated you feel. Connection is a fundamental human need, and it's okay to acknowledge when it's missing."
    ],
    "self_doubt": [
        "I want you to know that you are enough, exactly as you are right now.",
        "Self-doubt is something we all experience, but it doesn't reflect your true worth or potential.",
        "Those negative thoughts aren't facts. You have unique strengths and qualities that matter.",
        "It's easy to be our own harshest critics. Try to speak to yourself with the kindness you'd offer a good friend.",
        "Your worth isn't determined by your achievements or abilities. You have inherent value as a person."
    ],
    "default": [
        "Thank you for sharing that with me. It takes courage to express our deeper thoughts and feelings.",
        "I appreciate you opening up. Your reflections show thoughtfulness and self-awareness.",
        "That's a meaningful insight. These kinds of reflections help us understand ourselves better.",
        "I value you sharing something so personal. These thoughts and experiences shape who we are.",
        "Thank you for trusting me with that. Your willingness to explore these thoughts shows inner strength."
    ]
}

# Follow-up questions to encourage further reflection
FOLLOW_UP_QUESTIONS = {
    "past_experiences": [
        "How do you think that experience has shaped who you are today?",
        "What's one lesson you've carried forward from that time in your life?",
        "If you could talk to your younger self during that time, what would you say?"
    ],
    "self_reflection": [
        "What led you to this realization?",
        "How might this insight change things for you moving forward?",
        "What's one small step you could take based on this understanding?"
    ],
    "aspirations": [
        "What first inspired this goal or dream?",
        "What would achieving this mean to you personally?",
        "What's one small step you could take toward this vision?"
    ],
    "regrets": [
        "What would self-forgiveness look like in this situation?",
        "Is there anything positive that came from this difficult experience?",
        "How might this experience help you make different choices in the future?"
    ],
    "fears": [
        "What helps you cope when you're feeling this way?",
        "What would it look like to take one small step despite this fear?",
        "What's the worst that could happen, and how might you handle it if it did?"
    ],
    "gratitude": [
        "How does focusing on this positive aspect affect your overall outlook?",
        "What other small things in your life bring you similar feelings?",
        "How might you build on this positive experience or feeling?"
    ],
    "trauma": [
        "What has helped you cope with this difficult experience?",
        "Have you found any practices that help when memories of this arise?",
        "What would support and healing look like for you moving forward?"
    ],
    "loneliness": [
        "Are there any small connections in your day that bring you comfort?",
        "What kind of connection would feel most meaningful to you right now?",
        "Is there a community or group centered around your interests that might feel welcoming?"
    ],
    "self_doubt": [
        "What would you say to a friend who expressed these same doubts about themselves?",
        "Can you recall a time when you felt more confident? What was different then?",
        "What's one small thing you could do today to be kind to yourself?"
    ],
    "default": [
        "Would you like to share more about that?",
        "How have these thoughts been affecting you lately?",
        "What do you think would be a helpful next step for you?"
    ]
}

def detect_deep_thought(text):
    """
    Detect if the text contains deep thoughts or personal stories.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Detection results including category and matched patterns
    """
    text = text.lower()
    
    # Check for deep thought patterns
    matches = []
    for pattern in DEEP_THOUGHT_PATTERNS:
        if re.search(r'\b' + pattern + r'\b', text):
            matches.append(pattern)
    
    if not matches:
        return {"is_deep_thought": False}
    
    # Determine the category of the deep thought
    categories = []
    for category, keywords in THOUGHT_CATEGORIES.items():
        if any(keyword in text for keyword in keywords):
            categories.append(category)
    
    # Default to general category if no specific one is found
    if not categories:
        categories = ["default"]
    
    return {
        "is_deep_thought": True,
        "categories": categories,
        "matches": matches
    }

def generate_encouraging_response(deep_thought_info, include_follow_up=True):
    """
    Generate an encouraging response based on the detected deep thought.
    
    Args:
        deep_thought_info (dict): Information about the detected deep thought
        include_follow_up (bool): Whether to include a follow-up question
        
    Returns:
        str: An encouraging response
    """
    if not deep_thought_info.get("is_deep_thought", False):
        return None
    
    categories = deep_thought_info.get("categories", ["default"])
    primary_category = categories[0]  # Use the first category as primary
    
    # Select a random encouraging response for the primary category
    response = random.choice(ENCOURAGING_RESPONSES.get(primary_category, ENCOURAGING_RESPONSES["default"]))
    
    # Add a follow-up question if requested
    if include_follow_up:
        follow_up = random.choice(FOLLOW_UP_QUESTIONS.get(primary_category, FOLLOW_UP_QUESTIONS["default"]))
        response += f"\n\n{follow_up}"
    
    return response

def process_deep_thought(text):
    """
    Process text to detect deep thoughts and generate an encouraging response.
    
    Args:
        text (str): The user's message
        
    Returns:
        dict: Processing results including detection and response
    """
    deep_thought_info = detect_deep_thought(text)
    
    if not deep_thought_info.get("is_deep_thought", False):
        return {"is_deep_thought": False}
    
    response = generate_encouraging_response(deep_thought_info)
    
    return {
        "is_deep_thought": True,
        "categories": deep_thought_info.get("categories", ["default"]),
        "response": response
    }
