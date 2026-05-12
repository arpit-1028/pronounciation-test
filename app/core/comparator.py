from difflib import SequenceMatcher

# Expanded phoneme similarity map — phonemes that sound close to each other
# Used to give partial credit instead of marking as completely wrong
SIMILAR = {
    # Voiced ↔ Unvoiced pairs
    "t": ["d", "th"],
    "d": ["t", "dh"],
    "p": ["b"],
    "b": ["p", "v"],
    "k": ["g"],
    "g": ["k"],
    "f": ["v", "th"],
    "v": ["f", "b", "w"],
    "s": ["z", "sh", "th"],
    "z": ["s", "zh", "dh"],
    "sh": ["s", "zh", "ch"],
    "zh": ["sh", "z", "j"],
    "ch": ["sh", "j", "t"],
    "j": ["ch", "zh", "g"],
    "th": ["t", "f", "s", "dh"],
    "dh": ["d", "z", "th"],

    # Nasal similarities
    "n": ["ng", "m"],
    "ng": ["n", "m"],
    "m": ["n", "ng"],

    # Liquid/Glide similarities
    "r": ["l", "w"],
    "l": ["r", "n"],
    "w": ["v", "r", "u"],
    "y": ["i", "e"],

    # Vowel similarities (these are the most commonly confused)
    "a": ["e", "o", "u", "ai"],
    "e": ["a", "i"],
    "i": ["e", "y", "ee"],
    "o": ["a", "u", "au"],
    "u": ["o", "w", "oo"],

    # Diphthong similarities
    "ai": ["a", "e", "i"],
    "au": ["o", "a", "u"],
    "oi": ["o", "ai"],
}

def _is_similar(phoneme_a, phoneme_b):
    """Check if two phonemes are acoustically similar"""
    if phoneme_a == phoneme_b:
        return True
    if phoneme_a in SIMILAR and phoneme_b in SIMILAR[phoneme_a]:
        return True
    if phoneme_b in SIMILAR and phoneme_a in SIMILAR[phoneme_b]:
        return True
    return False

def compare(expected, spoken):
    results = []
    
    # Use SequenceMatcher to align the phoneme arrays intelligently
    # This prevents an extra sound at the beginning from breaking the whole word
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
                
                # Check if the mismatch is a similar-sounding phoneme
                if exp and spk and _is_similar(exp, spk):
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