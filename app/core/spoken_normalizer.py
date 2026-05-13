from app.phonemes.ipa_map import IPA_TO_INTERNAL

# Sort by length descending so multi-char IPA symbols are matched first
_SORTED_KEYS = sorted(IPA_TO_INTERNAL.keys(), key=len, reverse=True)

def normalize_spoken(phonemes):
    """Convert IPA phonemes to internal representation.
    Uses greedy matching for multi-character IPA symbols like aɪ, eɪ, oʊ.
    Unknown symbols are skipped with a warning log."""
    result = []
    for p in phonemes:
        matched = False
        remaining = p
        while remaining:
            found = False
            for key in _SORTED_KEYS:
                if remaining.startswith(key):
                    result.append(IPA_TO_INTERNAL[key])
                    remaining = remaining[len(key):]
                    found = True
                    break
            if not found:
                # Skip unknown character
                remaining = remaining[1:]
        if not matched and not result:
            pass  # silently skip empty
    return result