import { useState, useEffect, useRef, useCallback } from 'react';
import { AudioRecorder } from '../utils/audioUtils';

export default function PracticeView({ word, accent = 'auto', onResult, onError }) {
  const [status, setStatus] = useState('ready'); // ready | recording | processing
  const [timer, setTimer] = useState(0);
  const [bars, setBars] = useState(new Array(32).fill(4));
  const recorderRef = useRef(null);
  const timerRef = useRef(null);
  const animRef = useRef(null);

  // Text-to-Speech: let user hear correct pronunciation
  const handleListen = useCallback(() => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(word.display);
      utterance.lang = 'en-US';
      utterance.rate = 0.85;
      utterance.pitch = 1;
      window.speechSynthesis.speak(utterance);
    }
  }, [word]);

  // Waveform animation loop
  const animateWaveform = useCallback(() => {
    if (!recorderRef.current) return;
    const data = recorderRef.current.getFrequencyData();
    if (data.length > 0) {
      const step = Math.floor(data.length / 32);
      const newBars = [];
      for (let i = 0; i < 32; i++) {
        const val = data[i * step] || 0;
        newBars.push(Math.max(4, (val / 255) * 64));
      }
      setBars(newBars);
    }
    animRef.current = requestAnimationFrame(animateWaveform);
  }, []);

  // Start recording
  const startRecording = async () => {
    try {
      const recorder = new AudioRecorder();
      await recorder.start();
      recorderRef.current = recorder;
      setStatus('recording');
      setTimer(0);

      // Timer
      timerRef.current = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);

      // Waveform
      animRef.current = requestAnimationFrame(animateWaveform);
    } catch (err) {
      onError('Microphone access denied. Please allow microphone permission.');
    }
  };

  // Stop recording & send to API
  const stopRecording = async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (animRef.current) cancelAnimationFrame(animRef.current);
    setBars(new Array(32).fill(4));

    if (!recorderRef.current) return;

    setStatus('processing');

    try {
      const wavBlob = await recorderRef.current.stop();
      recorderRef.current = null;

      // Send to API
      const { checkPronunciation } = await import('../services/api.js');
      const result = await checkPronunciation(word.text, wavBlob, accent);
      onResult(result);
    } catch (err) {
      onError(err.message || 'Failed to process audio. Is the backend running?');
    }
  };

  // Auto-stop after 15 seconds
  useEffect(() => {
    if (status === 'recording' && timer >= 15) {
      stopRecording();
    }
  }, [timer, status]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (animRef.current) cancelAnimationFrame(animRef.current);
      if (recorderRef.current) recorderRef.current.cancel();
    };
  }, []);

  const formatTime = (s) => {
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (status === 'processing') {
    return (
      <div className="practice">
        <div className="practice__word">
          <div className="practice__word-label">Analyzing</div>
          <div className="practice__word-text">{word.display}</div>
        </div>
        <div className="processing">
          <div className="processing__spinner" />
          <div className="processing__text">AI is analyzing your pronunciation...</div>
          <div className="processing__subtext">This may take a few seconds</div>
        </div>
      </div>
    );
  }

  return (
    <div className="practice">
      {/* Word Display */}
      <div className="practice__word">
        <div className="practice__word-label">Pronounce this</div>
        <div className="practice__word-text">{word.display}</div>
        {word.phonemeHint && (
          <div className="practice__word-phoneme">{word.phonemeHint}</div>
        )}
        <button className="practice__listen-btn" onClick={handleListen}>
          🔊 Listen First
        </button>
      </div>

      {/* Mic Area */}
      <div className="mic-area">
        {status === 'recording' && (
          <div className="mic-timer">{formatTime(timer)}</div>
        )}

        <div style={{ position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {status === 'recording' && (
            <>
              <div className="mic-btn__ring mic-btn__ring--1" style={{ borderColor: 'rgba(239, 68, 68, 0.3)' }} />
              <div className="mic-btn__ring mic-btn__ring--2" style={{ borderColor: 'rgba(239, 68, 68, 0.3)' }} />
              <div className="mic-btn__ring mic-btn__ring--3" style={{ borderColor: 'rgba(239, 68, 68, 0.3)' }} />
            </>
          )}
          <button
            className={`mic-btn ${status === 'recording' ? 'mic-btn--recording' : ''}`}
            onClick={status === 'recording' ? stopRecording : startRecording}
            aria-label={status === 'recording' ? 'Stop recording' : 'Start recording'}
          >
            {status === 'recording' ? '⏹' : '🎤'}
          </button>
        </div>

        <div className="mic-label">
          {status === 'recording'
            ? 'Tap to stop recording'
            : 'Tap to start recording'}
        </div>
      </div>

      {/* Waveform */}
      <div className={`waveform ${status === 'recording' ? 'waveform--active' : ''}`}>
        {bars.map((h, i) => (
          <div
            key={i}
            className="waveform__bar"
            style={{ height: `${h}px` }}
          />
        ))}
      </div>
    </div>
  );
}
