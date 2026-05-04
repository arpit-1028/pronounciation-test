SIMILAR = {
    "n": ["ng"],
    "ng": ["n"],
    "e": ["a"],
    "a": ["e"],
    "i": ["e"],
}

def compare(expected, spoken):
    results = []
    min_len = min(len(expected), len(spoken))

    for i in range(min_len):
        if expected[i] == spoken[i]:
            results.append({"type": "correct"})
        else:
            results.append({"type": "wrong"})

    # missing sounds
    if len(expected) > len(spoken):
        for _ in range(len(expected) - len(spoken)):
            results.append({"type": "missing"})

    # extra sounds
    if len(spoken) > len(expected):
        for _ in range(len(spoken) - len(expected)):
            results.append({"type": "extra"})

    return results