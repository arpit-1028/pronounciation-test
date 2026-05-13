# =============================================================
#  Indian English Accent Configuration
#  Defines systematic phoneme equivalences for General Indian English
# =============================================================

# Phoneme pairs where Indian English speakers systematically substitute
# one sound for another. These are NOT errors — they are valid accent features.
#
# Format: { "standard_phoneme": ["indian_equivalent_1", "indian_equivalent_2"] }
#
# Sources:
#   - Bansal & Harrison (1994) "Spoken English for India"
#   - CIEFL Hyderabad phonology studies
#   - Wells (2008) "Longman Pronunciation Dictionary" (Indian English notes)

INDIAN_ENGLISH_EQUIVALENCES = {
    # ─── Dental Fricatives → Plosives (Most common Indian English feature) ───
    # Indian speakers replace θ/ð with aspirated/unaspirated dental stops
    "th": ["t"],          # "think" → "tink", "three" → "tree"
    "dh": ["d"],          # "this" → "dis", "that" → "dat"

    # ─── V/W merger ───
    # Many Indian speakers don't distinguish /v/ and /w/
    "v": ["w"],           # "very" → "wery"
    "w": ["v"],           # "west" → "vest"

    # ─── Vowel adjustments ───
    # Indian English has a simpler vowel inventory
    "a": ["e", "o", "u"],          # Schwa often becomes full vowel
    "e": ["a", "i"],               # Short e ↔ short a/i
    "i": ["e", "ee"],              # Tense/lax merger
    "o": ["a", "u", "au"],         # /ɒ/ → /ɔ/ or /ɑ/
    "u": ["o", "oo"],              # Short u ↔ short o

    # ─── Rhotic R ───
    # Indian English is fully rhotic (pronounces all R's)
    # This means Indian speakers ADD 'r' where British drops it
    # (handled in comparator as "extra" tolerance)

    # ─── Retroflex consonants ───
    # Indian t/d are often retroflex (ʈ/ɖ) but map to same internal phoneme
    "t": ["d"],
    "d": ["t"],

    # ─── Sibilant adjustments ───
    "z": ["s", "j"],       # Sometimes /z/ → /s/ or /dʒ/
    "sh": ["s"],           # Some speakers: "ship" closer to "sip"

    # ─── Other common patterns ───
    "f": ["ph"],           # Aspirated p for f in some varieties
    "j": ["z", "ch"],      # /dʒ/ variation
}

# Words where Indian English has a completely different stress/phoneme pattern
# These override the standard expected phonemes entirely
INDIAN_PRONUNCIATION_OVERRIDES = {
    # Word: Indian English phoneme sequence
    "schedule":     ["s", "k", "e", "j", "u", "l"],          # "skedule" not "shedule"
    "vitamin":      ["v", "i", "t", "a", "m", "i", "n"],     # Flat vowels
    "data":         ["d", "e", "t", "a"],                     # "day-ta" not "dah-ta"
    "tomato":       ["t", "o", "m", "e", "t", "o"],           # "to-may-to"
    "garage":       ["g", "a", "r", "a", "j"],                # Stress on first syllable
    "advertisement":["a", "d", "v", "r", "t", "ai", "z", "m", "a", "n", "t"],
    "lieutenant":   ["l", "e", "f", "t", "e", "n", "a", "n", "t"],  # British pronunciation
    "aluminium":    ["a", "l", "u", "m", "i", "n", "i", "a", "m"],
    "mobile":       ["m", "o", "b", "ai", "l"],               # "mo-bile" not "mo-bul"
}

# These phoneme substitutions should be treated as "accent_match" (full credit)
# rather than "similar" (partial credit) when accent=indian
ACCENT_FULL_CREDIT_PAIRS = {
    ("th", "t"),    # "think" → "tink" is standard Indian English
    ("dh", "d"),    # "this" → "dis" is standard Indian English
    ("v", "w"),     # V/W merger
    ("w", "v"),     # V/W merger (reverse)
    ("t", "d"),     # Retroflex unvoicing variation
    ("d", "t"),     # Retroflex voicing variation
}
