from difflib import SequenceMatcher

SIMILAR = {
    "n": ["ng"],
    "ng": ["n"],
    "e": ["a"],
    "a": ["e"],
    "i": ["e"],
}

def compare(expected, spoken):
    results = []
    
    # Use SequenceMatcher to align the phoneme arrays intelligently
    # This prevents an extra sound at the beginning from breaking the whole word
    sm = SequenceMatcher(None, expected, spoken)
    
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                results.append({"type": "correct", "expected": expected[i1 + k], "spoken": spoken[j1 + k]})
        elif tag == 'replace':
            max_len = max(i2 - i1, j2 - j1)
            for k in range(max_len):
                exp = expected[i1 + k] if (i1 + k) < i2 else None
                spk = spoken[j1 + k] if (j1 + k) < j2 else None
                results.append({"type": "wrong", "expected": exp, "spoken": spk})
        elif tag == 'delete':
            for k in range(i1, i2):
                results.append({"type": "missing", "expected": expected[k], "spoken": None})
        elif tag == 'insert':
            for k in range(j1, j2):
                results.append({"type": "extra", "expected": None, "spoken": spoken[k]})

    return results