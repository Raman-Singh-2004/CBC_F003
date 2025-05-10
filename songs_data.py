"""
Song recommendations database for different moods.
Each mood has a list of songs with title, artist, and a YouTube search link.
"""

SONGS_BY_MOOD = {
    "happy": [
        {
            "title": "Happy",
            "artist": "Pharrell Williams",
            "link": "https://www.youtube.com/results?search_query=pharrell+williams+happy"
        },
        {
            "title": "Can't Stop the Feeling",
            "artist": "Justin Timberlake",
            "link": "https://www.youtube.com/results?search_query=justin+timberlake+cant+stop+the+feeling"
        },
        {
            "title": "Uptown Funk",
            "artist": "Mark Ronson ft. Bruno Mars",
            "link": "https://www.youtube.com/results?search_query=mark+ronson+uptown+funk"
        },
        {
            "title": "Good as Hell",
            "artist": "Lizzo",
            "link": "https://www.youtube.com/results?search_query=lizzo+good+as+hell"
        },
        {
            "title": "Walking on Sunshine",
            "artist": "Katrina & The Waves",
            "link": "https://www.youtube.com/results?search_query=katrina+and+the+waves+walking+on+sunshine"
        }
    ],
    "sad": [
        {
            "title": "Someone Like You",
            "artist": "Adele",
            "link": "https://www.youtube.com/results?search_query=adele+someone+like+you"
        },
        {
            "title": "Fix You",
            "artist": "Coldplay",
            "link": "https://www.youtube.com/results?search_query=coldplay+fix+you"
        },
        {
            "title": "Hurt",
            "artist": "Johnny Cash",
            "link": "https://www.youtube.com/results?search_query=johnny+cash+hurt"
        },
        {
            "title": "Everybody Hurts",
            "artist": "R.E.M.",
            "link": "https://www.youtube.com/results?search_query=rem+everybody+hurts"
        },
        {
            "title": "Nothing Compares 2 U",
            "artist": "Sinéad O'Connor",
            "link": "https://www.youtube.com/results?search_query=sinead+oconnor+nothing+compares+2u"
        }
    ],
    "calm": [
        {
            "title": "Weightless",
            "artist": "Marconi Union",
            "link": "https://www.youtube.com/results?search_query=marconi+union+weightless"
        },
        {
            "title": "Claire de Lune",
            "artist": "Claude Debussy",
            "link": "https://www.youtube.com/results?search_query=debussy+claire+de+lune"
        },
        {
            "title": "Gymnopédie No.1",
            "artist": "Erik Satie",
            "link": "https://www.youtube.com/results?search_query=erik+satie+gymnopedie+no+1"
        },
        {
            "title": "Breathe",
            "artist": "Télépopmusik",
            "link": "https://www.youtube.com/results?search_query=telepopmusik+breathe"
        },
        {
            "title": "Porcelain",
            "artist": "Moby",
            "link": "https://www.youtube.com/results?search_query=moby+porcelain"
        }
    ],
    "energetic": [
        {
            "title": "Eye of the Tiger",
            "artist": "Survivor",
            "link": "https://www.youtube.com/results?search_query=survivor+eye+of+the+tiger"
        },
        {
            "title": "Stronger",
            "artist": "Kanye West",
            "link": "https://www.youtube.com/results?search_query=kanye+west+stronger"
        },
        {
            "title": "Don't Stop Me Now",
            "artist": "Queen",
            "link": "https://www.youtube.com/results?search_query=queen+dont+stop+me+now"
        },
        {
            "title": "Titanium",
            "artist": "David Guetta ft. Sia",
            "link": "https://www.youtube.com/results?search_query=david+guetta+sia+titanium"
        },
        {
            "title": "Till I Collapse",
            "artist": "Eminem",
            "link": "https://www.youtube.com/results?search_query=eminem+till+i+collapse"
        }
    ],
    "focused": [
        {
            "title": "Experience",
            "artist": "Ludovico Einaudi",
            "link": "https://www.youtube.com/results?search_query=ludovico+einaudi+experience"
        },
        {
            "title": "Time",
            "artist": "Hans Zimmer",
            "link": "https://www.youtube.com/results?search_query=hans+zimmer+time"
        },
        {
            "title": "Strobe",
            "artist": "Deadmau5",
            "link": "https://www.youtube.com/results?search_query=deadmau5+strobe"
        },
        {
            "title": "Intro",
            "artist": "The xx",
            "link": "https://www.youtube.com/results?search_query=the+xx+intro"
        },
        {
            "title": "Comptine d'un autre été",
            "artist": "Yann Tiersen",
            "link": "https://www.youtube.com/results?search_query=yann+tiersen+comptine+dun+autre+ete"
        }
    ],
    "relaxed": [
        {
            "title": "Somewhere Over The Rainbow",
            "artist": "Israel Kamakawiwo'ole",
            "link": "https://www.youtube.com/results?search_query=israel+kamakawiwoole+somewhere+over+the+rainbow"
        },
        {
            "title": "Three Little Birds",
            "artist": "Bob Marley",
            "link": "https://www.youtube.com/results?search_query=bob+marley+three+little+birds"
        },
        {
            "title": "Here Comes the Sun",
            "artist": "The Beatles",
            "link": "https://www.youtube.com/results?search_query=the+beatles+here+comes+the+sun"
        },
        {
            "title": "Banana Pancakes",
            "artist": "Jack Johnson",
            "link": "https://www.youtube.com/results?search_query=jack+johnson+banana+pancakes"
        },
        {
            "title": "Don't Worry Be Happy",
            "artist": "Bobby McFerrin",
            "link": "https://www.youtube.com/results?search_query=bobby+mcferrin+dont+worry+be+happy"
        }
    ]
}

def get_song_recommendations(mood, count=3):
    """
    Get song recommendations for a specific mood.
    
    Args:
        mood (str): The mood to get songs for (happy, sad, calm, energetic, focused, relaxed)
        count (int): Number of songs to return (default: 3)
        
    Returns:
        list: List of song dictionaries or empty list if mood not found
    """
    import random
    
    # Normalize the mood input
    mood = mood.lower().strip()
    
    # Map similar moods to our categories
    mood_mapping = {
        # Happy variants
        "joy": "happy",
        "excited": "happy",
        "cheerful": "happy",
        "joyful": "happy",
        "upbeat": "happy",
        "good": "happy",
        "great": "happy",
        
        # Sad variants
        "depressed": "sad",
        "unhappy": "sad",
        "down": "sad",
        "blue": "sad",
        "gloomy": "sad",
        "melancholy": "sad",
        "upset": "sad",
        
        # Calm variants
        "peaceful": "calm",
        "serene": "calm",
        "tranquil": "calm",
        "quiet": "calm",
        "gentle": "calm",
        
        # Energetic variants
        "active": "energetic",
        "lively": "energetic",
        "dynamic": "energetic",
        "vigorous": "energetic",
        "pumped": "energetic",
        "motivated": "energetic",
        
        # Focused variants
        "concentrated": "focused",
        "attentive": "focused",
        "productive": "focused",
        "studying": "focused",
        "work": "focused",
        
        # Relaxed variants
        "chill": "relaxed",
        "mellow": "relaxed",
        "easy": "relaxed",
        "laid-back": "relaxed",
        "comfortable": "relaxed"
    }
    
    # Map the mood if it's a variant
    if mood in mood_mapping:
        mood = mood_mapping[mood]
    
    # Get songs for the mood
    if mood in SONGS_BY_MOOD:
        songs = SONGS_BY_MOOD[mood]
        # Return random selection if we have more songs than requested
        if len(songs) > count:
            return random.sample(songs, count)
        return songs
    
    # If mood not found, return empty list
    return []
