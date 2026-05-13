from difflib import SequenceMatcher

# Expanded phoneme similarity map — phonemes that sound close to each other
# Used to give partial credit instead of marking as completely wrong
SIMILAR = {
    # Voiced ↔ Unvoiced pairs
    "t": ["d", "th", "dh"],
    "d": ["t", "dh", "th"],
    "p": ["b", "f"],
    "b": ["p", "v", "m"],
    "k": ["g", "ch"],
    "g": ["k", "j"],
    "f": ["v", "th", "p"],
    "v": ["f", "b", "w"],
    "s": ["z", "sh", "th"],
    "z": ["s", "zh", "dh", "j"],
    "sh": ["s", "zh", "ch"],
    "zh": ["sh", "z", "j"],
    "ch": ["sh", "j", "t", "k"],
    "j": ["ch", "zh", "g", "z"],
    "th": ["t", "f", "s", "dh"],
    "dh": ["d", "z", "th", "t"],
    "h": ["a"],

    # Nasal similarities
    "n": ["ng", "m", "d"],
    "ng": ["n", "m", "g"],
    "m": ["n", "ng", "b"],

    # Liquid/Glide similarities
    "r": ["l", "w", "d"],
    "l": ["r", "n", "w"],
    "w": ["v", "r", "u", "o"],
    "y": ["i", "e", "j"],

    # Vowel similarities (most commonly confused)
    "a": ["e", "o", "u", "ai", "au"],
    "e": ["a", "i", "ai"],
    "i": ["e", "y", "ee", "a"],
    "o": ["a", "u", "au", "oi"],
    "u": ["o", "w", "oo", "a"],

    # Diphthong similarities
    "ai": ["a", "e", "i", "oi"],
    "au": ["o", "a", "u", "aw"],
    "oi": ["o", "ai", "i"],
    "ee": ["i", "e"],
    "oo": ["u", "o"],
    "aw": ["au", "o", "a"],
}

# Vowel set for weighted scoring
VOWELS = {"a", "e", "i", "o", "u", "ai", "au", "oi", "ee", "oo", "aw"}

def _is_similar(phoneme_a, phoneme_b):
    """Check if two phonemes are acoustically similar"""
    if phoneme_a == phoneme_b:
        return True
    if phoneme_a in SIMILAR and phoneme_b in SIMILAR[phoneme_a]:
        return True
    if phoneme_b in SIMILAR and phoneme_a in SIMILAR[phoneme_b]:
        return True
    return False

def _is_accent_match(phoneme_a, phoneme_b, accent="auto"):
    """Check if the mismatch is a known accent pattern (full credit)"""
    if accent not in ("indian", "auto"):
        return False
    from app.core.accent_config import ACCENT_FULL_CREDIT_PAIRS
    pair = (phoneme_a, phoneme_b)
    reverse = (phoneme_b, phoneme_a)
    return pair in ACCENT_FULL_CREDIT_PAIRS or reverse in ACCENT_FULL_CREDIT_PAIRS

def compare(expected, spoken, accent="auto"):
    results = []

    sm = SequenceMatcher(None, expected, spoken)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                results.append({
                    "type": "correct",
                    "expected": expected[i1 + k],
                    "spoken": spoken[j1 + k]
                })
        elif tag == 'replace':
            max_len = max(i2 - i1, j2 - j1)
            for k in range(max_len):
                exp = expected[i1 + k] if (i1 + k) < i2 else None
                spk = spoken[j1 + k] if (j1 + k) < j2 else None

                if exp and spk and exp == spk:
                    results.append({
                        "type": "correct",
                        "expected": exp,
                        "spoken": spk
                    })
                elif exp and spk and _is_accent_match(exp, spk, accent):
                    # Known accent pattern — treat as correct
                    results.append({
                        "type": "accent_match",
                        "expected": exp,
                        "spoken": spk
                    })
                elif exp and spk and _is_similar(exp, spk):
                    results.append({
                        "type": "similar",
                        "expected": exp,
                        "spoken": spk
                    })
                elif exp and not spk:
                    results.append({
                        "type": "missing",
                        "expected": exp,
                        "spoken": None
                    })
                elif spk and not exp:
                    results.append({
                        "type": "extra",
                        "expected": None,
                        "spoken": spk
                    })
                else:
                    results.append({
                        "type": "wrong",
                        "expected": exp,
                        "spoken": spk
                    })
        elif tag == 'delete':
            for k in range(i1, i2):
                results.append({
                    "type": "missing",
                    "expected": expected[k],
                    "spoken": None
                })
        elif tag == 'insert':
            for k in range(j1, j2):
                results.append({
                    "type": "extra",
                    "expected": None,
                    "spoken": spoken[k]
                })

    return results