const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Send recorded audio to the backend for pronunciation checking
 * @param {string} word - The target word/sentence
 * @param {Blob} audioBlob - WAV audio blob
 * @param {string} accent - Accent mode: "auto", "indian", or "british"
 * @returns {Promise<Object>} - Score, feedback, comparison data
 */
export async function checkPronunciation(word, audioBlob, accent = 'auto') {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  const response = await fetch(
    `${API_URL}/check/${encodeURIComponent(word)}?accent=${accent}`,
    {
      method: 'POST',
      body: formData,
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Server error: ${response.status} — ${errorText}`);
  }

  return response.json();
}
