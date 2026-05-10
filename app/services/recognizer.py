import os
import platform

# Help phonemizer find eSpeak on Windows before importing transformers
if platform.system() == "Windows":
    os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
    os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa
import soundfile as sf
import numpy as np

# Load the Wav2Vec2 model fine-tuned for phoneme recognition
MODEL_ID = "facebook/wav2vec2-xlsr-53-espeak-cv-ft"
processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

def preprocess_audio(input_file, output_file="clean.wav"):
    audio, sr = librosa.load(input_file, sr=16000)

    # Use a much less aggressive trim (top_db=60 instead of 25) so quiet consonants like 'p' aren't cut off
    trimmed, _ = librosa.effects.trim(audio, top_db=60)

    # normalize the audio volume
    if np.max(np.abs(trimmed)) > 0:
        trimmed = trimmed / np.max(np.abs(trimmed))

    sf.write(output_file, trimmed, 16000)
    return output_file, trimmed

def recognize_audio(filename):
    clean_file, speech_array = preprocess_audio(filename)

    print("PROCESSING FILE:", clean_file)

    # Process audio with Wav2Vec2
    inputs = processor(speech_array, sampling_rate=16000, return_tensors="pt")
    
    with torch.no_grad():
        logits = model(inputs.input_values).logits
        
    # Decode the most likely phonemes
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    
    # transcription returns a list of strings, we take the first element
    phonemes_str = transcription[0]
    
    print("RAW PHONEMES:", phonemes_str)

    # Return as a list of individual phonemes, just like Allosaurus did
    return phonemes_str.split() if phonemes_str else []