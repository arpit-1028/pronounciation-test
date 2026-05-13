# Vowels matter more than consonants for intelligibility
VOWELS = {"a", "e", "i", "o", "u", "ai", "au", "oi", "ee", "oo", "aw"}

def score(results):
    total_weight = 0
    points = 0

    for r in results:
        # Determine phoneme for weighting
        phoneme = r.get("expected") or r.get("spoken") or "x"
        weight = 1.5 if phoneme in VOWELS else 1.0
        total_weight += weight

        if r["type"] == "correct":
            points += weight * 1.0
        elif r["type"] == "accent_match":
            # Known accent pattern — full credit
            points += weight * 1.0
        elif r["type"] == "similar":
            # Acoustically similar — generous partial credit
            points += weight * 0.65
        elif r["type"] == "wrong":
            # Completely wrong — small credit
            points += weight * 0.15
        elif r["type"] == "missing":
            points += 0
        elif r["type"] == "extra":
            points += 0

    if total_weight == 0:
        return 0

    return round((points / total_weight) * 100, 2)