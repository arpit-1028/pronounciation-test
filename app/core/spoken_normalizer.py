from app.phonemes.ipa_map import IPA_TO_INTERNAL

def normalize_spoken(phonemes):
    result = []
    for p in phonemes:
        if p in IPA_TO_INTERNAL:
            result.append(IPA_TO_INTERNAL[p])
    return result