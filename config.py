# Configuration for wordlist detection and responses

WORDLIST_CONFIG = {
    "aja_sendiri": {
        "keywords": ["aja", "sendiri"],
        "image": "assets/aja-sendiri.jpg",
        "fuzzy_words": {
            "aja": ["aja", "aj", "aa", "ja", "ajaa", "aaja", "amja"],
            "sendiri": ["sendiri", "sndiri", "sendri", "seniri", "semdiri"]
        }
    },
    "sehat": {
        "keywords": ["sehat"],
        "image": "assets/sehat.jpg",
        "fuzzy_words": {
            "sehat": ["sehat"]
        }
    },
    "edan": {
        "keywords": ["edan"],
        "image": "assets/edan.jpg",
        "fuzzy_words": {
            "edan": ["edan"]
        }
    }
}

# Character replacements for leet speak
CHAR_REPLACEMENTS = {
    '4': 'a', '@': 'a', '^': 'a',
    '3': 'e', 
    '1': 'i', '!': 'i', '|': 'i',
    '0': 'o',
    '5': 's', '$': 's',
    '7': 't', '+': 't',
    '8': 'b', '6': 'g'
}

# Voice channel configuration
VOICE_CONFIG = {
    "audio_file": "assets/loop-audio.mp3",
    "bitrate": 128,
    "volume": 0.05  # Very quiet background (5%)
}