
# AI Speech Coach 🎙️

An AI-powered pronunciation assessment system that analyzes spoken audio, converts speech into phonemes using Wav2Vec2, and provides pronunciation accuracy scores with feedback.

## Features

* Speech-to-phoneme conversion
* Pronunciation accuracy scoring
* AI-powered speech recognition
* Real-time pronunciation feedback
* FastAPI backend
* Hugging Face Transformers integration
* Audio preprocessing using Librosa
* Phoneme comparison system

---

# Tech Stack

* Python
* FastAPI
* PyTorch
* Transformers
* Wav2Vec2
* Librosa
* Phonemizer
* Hugging Face

---

# Project Workflow

1. User uploads speech audio
2. Audio preprocessing is performed
3. Wav2Vec2 model extracts phonemes
4. Expected and spoken phonemes are compared
5. Pronunciation score is generated
6. Feedback is returned through API

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/speech-coach.git
cd speech-coach
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install eSpeak NG

Download and install eSpeak NG:

https://github.com/espeak-ng/espeak-ng/releases

Recommended installation path:

```text
C:\Program Files\eSpeak NG
```

---

# Run Project

```bash
python -m uvicorn app.main:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

# Example API Response

```json
{
  "expected_word": "learning",
  "spoken": ["l", "er", "n", "ih", "ng"],
  "score": 80,
  "feedback": ["Good pronunciation"]
}
```

---

# Deployment

This project can be deployed on:

* Hugging Face Spaces
* Render
* Railway
* Docker
* AWS

---

# Future Improvements

* Real-time microphone support
* Accent detection
* Waveform visualization
* IELTS speaking evaluation
* Multi-language pronunciation support
* Mobile app integration

---


title: Pronunciation Coach Api
emoji: 📉
colorFrom: pink
colorTo: red
sdk: docker
pinned: false


Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
 37fc6e61781b0c32522b5169268bc80be86bae92
