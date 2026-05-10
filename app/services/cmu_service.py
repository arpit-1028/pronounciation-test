import nltk
from nltk.corpus import cmudict

# Automatically download cmudict if not present on the deployment server
try:
    nltk.data.find('corpora/cmudict')
except LookupError:
    nltk.download('cmudict')

d = cmudict.dict()

def get_phonemes(word: str):
    word = word.lower()
    if word in d:
        return d[word][0]
    return []