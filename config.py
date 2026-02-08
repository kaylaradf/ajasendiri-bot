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
    "audio_file": "assets/loop-audio.mp3",  # Audio file to loop
    "channel_id": None,  # Set your voice channel ID here (optional)
    "bitrate": 128,  # Audio quality in kbps (64, 96, 128, 192, 256, 320)
    "volume": 0.15  # Volume level (0.0 - 1.0, default 0.15 for background opacity)
}