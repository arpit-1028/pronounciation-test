from fastapi import FastAPI, UploadFile, File

from app.services.cmu_service import get_phonemes
from app.phonemes.cmu_map import CMU_TO_INTERNAL
from app.core.normalizer import normalize
from app.core.comparator import compare
from app.core.scorer import score
from app.core.feedback import generate_feedback
from app.services.recognizer import recognize_audio
from app.phonemes.word_dict import WORD_DICT
from app.core.matcher import find_best_match

import shutil

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Pronunciation Engine Running"}

@app.post("/check/{word}")
async def check(word: str, audio: UploadFile = File(...)):
    
    print("CHECK ENDPOINT HIT")

    # Step 1: save uploaded audio file
    file_path = "input.wav"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    print("FILE SAVED:", file_path)

    # Step 2: expected pronunciation
    expected_cmu = get_phonemes(word)
    expected = normalize(expected_cmu, CMU_TO_INTERNAL)

    print("CMU RAW:", expected_cmu)
    print("EXPECTED:", expected)

    # Step 3: convert audio → phonemes
    from app.core.spoken_normalizer import normalize_spoken

    print("CALLING RECOGNIZER...")
    spoken_raw = recognize_audio(file_path)
    print("RAW SPOKEN:", spoken_raw)

    spoken = normalize_spoken(spoken_raw)
    print("NORMALIZED SPOKEN:", spoken)

    best_word,sc,results=find_best_match(spoken, WORD_DICT)
    fb=generate_feedback(results)

    # Step 5: score
    sc = score(results)

    # Step 6: feedback
    fb = generate_feedback(results)

    return {
    "expected_word": word,
    "detected_word": best_word,
    "spoken": spoken,
    "score": sc,
    "feedback": fb
}