from allosaurus.app import read_recognizer
import librosa
import soundfile as sf
import numpy as np

model = read_recognizer()

def preprocess_audio(input_file, output_file="clean.wav"):
    audio, sr = librosa.load(input_file, sr=16000)

    # moderate trimming
    trimmed, _ = librosa.effects.trim(audio, top_db=25)

    # normalize
    if np.max(np.abs(trimmed)) > 0:
        trimmed = trimmed / np.max(np.abs(trimmed))

    sf.write(output_file, trimmed, 16000)
    return output_file

def recognize_audio(filename):
    clean_file = preprocess_audio(filename)

    print("PROCESSING FILE:", clean_file)

    phonemes = model.recognize(clean_file)

    print("RAW PHONEMES:", phonemes)

    return phonemes.split() if phonemes else []