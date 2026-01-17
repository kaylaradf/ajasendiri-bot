# Configuration for wordlist detection and responses

WORDLIST_CONFIG = {
    "aja_sendiri": {
        "keywords": ["aja", "sendiri"],
        "image": "assets/aja-sendiri.jpg",
        "pattern": r'.*a.*j.*a.*s.*e.*n.*d.*i.*r.*i.*',
        "fuzzy_words": {
            "aja": ["aja", "aj", "aa", "ja", "ajaa", "aaja", "amja"],
            "sendiri": ["sendiri", "sndiri", "sendri", "seniri", "semdiri"]
        }
    },
    "sehat": {
        "keywords": ["sehat"],
        "image": "assets/sehat.jpg",
        "pattern": r'.*s.*e.*h.*a.*t.*',
        "fuzzy_words": {
            "sehat": ["sehat"]
        }
    },
    "edan": {
        "keywords": ["edan"],
        "image": "assets/edan.jpg",
        "pattern": r'.*e.*d.*a.*n.*',
        "fuzzy_words": {
            "edan": ["edan"]
        }
    }
    # Add more wordlists here:
    # "example": {
    #     "keywords": ["word1", "word2"],
    #     "image": "assets/example.jpg",
    #     "pattern": r'.*w.*o.*r.*d.*1.*w.*o.*r.*d.*2.*',
    #     "fuzzy_words": {
    #         "word1": ["word1", "wrd1", "w0rd1"],
    #         "word2": ["word2", "wrd2", "w0rd2"]
    #     }
    # }
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