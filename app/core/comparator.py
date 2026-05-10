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
            for _ in range(i1, i2):
                results.append({"type": "correct"})
        elif tag == 'replace':
            for _ in range(i1, i2):
                results.append({"type": "wrong"})
        elif tag == 'delete':
            for _ in range(i1, i2):
                results.append({"type": "missing"})
        elif tag == 'insert':
            for _ in range(j1, j2):
                results.append({"type": "extra"})

    return results