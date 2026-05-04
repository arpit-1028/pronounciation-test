from nltk.corpus import cmudict

d = cmudict.dict()

def get_phonemes(word: str):
    word = word.lower()
    if word in d:
        return d[word][0]
    return []