/**
 * AudioRecorder — records mic audio, provides waveform data,
 * and exports as 16kHz mono WAV for the backend.
 */
export class AudioRecorder {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.stream = null;
    this.analyser = null;
    this.audioContext = null;
    this.source = null;
  }

  /** Request mic and start recording */
  async start() {
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        sampleRate: 16000,
      }
    });

    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.source = this.audioContext.createMediaStreamSource(this.stream);
    this.analyser = this.audioContext.createAnalyser();
    this.analyser.fftSize = 256;
    this.source.connect(this.analyser);

    this.mediaRecorder = new MediaRecorder(this.stream);
    this.audioChunks = [];

    this.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) this.audioChunks.push(e.data);
    };

    this.mediaRecorder.start();
  }

  /** Get frequency data for waveform visualization */
  getFrequencyData() {
    if (!this.analyser) return new Uint8Array(0);
    const data = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteFrequencyData(data);
    return data;
  }

  /** Get time-domain waveform data */
  getWaveformData() {
    if (!this.analyser) return new Uint8Array(0);
    const data = new Uint8Array(this.analyser.frequencyBinCount);
    this.analyser.getByteTimeDomainData(data);
    return data;
  }

  /** Stop recording and return a WAV Blob */
  stop() {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') {
        reject(new Error('Recorder not active'));
        return;
      }

      this.mediaRecorder.onstop = async () => {
        try {
          const webmBlob = new Blob(this.audioChunks, { type: this.mediaRecorder.mimeType });
          const wavBlob = await this._convertToWav(webmBlob);
          this._cleanup();
          resolve(wavBlob);
        } catch (err) {
          this._cleanup();
          reject(err);
        }
      };

      this.mediaRecorder.stop();
    });
  }

  /** Cancel recording without producing output */
  cancel() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }
    this._cleanup();
  }

  /** Convert any audio blob → 16kHz mono WAV */
  async _convertToWav(blob) {
    const arrayBuffer = await blob.arrayBuffer();
    const ctx = new (window.OfflineAudioContext || window.webkitOfflineAudioContext)(1, 1, 16000);

    let audioBuffer;
    try {
      audioBuffer = await ctx.decodeAudioData(arrayBuffer);
    } catch {
      // Fallback: try a regular AudioContext
      const tempCtx = new (window.AudioContext || window.webkitAudioContext)();
      audioBuffer = await tempCtx.decodeAudioData(arrayBuffer);
      tempCtx.close();
    }

    // Resample to 16kHz mono
    const targetSampleRate = 16000;
    const offlineCtx = new OfflineAudioContext(1, Math.ceil(audioBuffer.duration * targetSampleRate), targetSampleRate);
    const bufferSource = offlineCtx.createBufferSource();
    bufferSource.buffer = audioBuffer;
    bufferSource.connect(offlineCtx.destination);
    bufferSource.start(0);

    const renderedBuffer = await offlineCtx.startRendering();
    const samples = renderedBuffer.getChannelData(0);

    return this._encodeWav(samples, targetSampleRate);
  }

  /** Encode Float32Array samples as WAV Blob */
  _encodeWav(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    // RIFF header
    this._writeStr(view, 0, 'RIFF');
    view.setUint32(4, 36 + samples.length * 2, true);
    this._writeStr(view, 8, 'WAVE');

    // fmt chunk
    this._writeStr(view, 12, 'fmt ');
    view.setUint32(16, 16, true);           // chunk size
    view.setUint16(20, 1, true);            // PCM format
    view.setUint16(22, 1, true);            // mono
    view.setUint32(24, sampleRate, true);    // sample rate
    view.setUint32(28, sampleRate * 2, true); // byte rate
    view.setUint16(32, 2, true);            // block align
    view.setUint16(34, 16, true);           // bits per sample

    // data chunk
    this._writeStr(view, 36, 'data');
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
      offset += 2;
    }

    return new Blob([buffer], { type: 'audio/wav' });
  }

  _writeStr(view, offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  _cleanup() {
    if (this.stream) {
      this.stream.getTracks().forEach(t => t.stop());
      this.stream = null;
    }
    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close();
      this.audioContext = null;
    }
    this.analyser = null;
    this.source = null;
    this.mediaRecorder = null;
    this.audioChunks = [];
  }
}
