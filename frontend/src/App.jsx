import { useState, useCallback } from 'react';
import Header from './components/Header';
import WordSelector from './components/WordSelector';
import PracticeView from './components/PracticeView';
import ResultsView from './components/ResultsView';
import { wordCategories } from './data/words';

export default function App() {
  const [view, setView] = useState('home'); // home | practice | results | error
  const [selectedWord, setSelectedWord] = useState(null);
  const [activeCategory, setActiveCategory] = useState(wordCategories[0].id);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [accent, setAccent] = useState('auto'); // auto | indian | british

  // Navigate to practice screen
  const handleSelectWord = useCallback((word) => {
    setSelectedWord(word);
    setResult(null);
    setError('');
    setView('practice');
  }, []);

  // Go back to home
  const handleBack = useCallback(() => {
    setView('home');
    setSelectedWord(null);
    setResult(null);
    setError('');
  }, []);

  // Receive result from PracticeView
  const handleResult = useCallback((data) => {
    setResult(data);
    setView('results');
  }, []);

  // Handle errors
  const handleError = useCallback((msg) => {
    setError(msg);
    setView('error');
  }, []);

  // Try again with same word
  const handleTryAgain = useCallback(() => {
    setResult(null);
    setError('');
    setView('practice');
  }, []);

  // Pick next word in the current category
  const handleNextWord = useCallback(() => {
    const cat = wordCategories.find(c => c.id === activeCategory);
    if (!cat) return handleBack();

    const currentIdx = cat.items.findIndex(w => w.text === selectedWord?.text);
    const nextIdx = (currentIdx + 1) % cat.items.length;
    handleSelectWord(cat.items[nextIdx]);
  }, [activeCategory, selectedWord, handleSelectWord, handleBack]);

  return (
    <>
      <Header view={view} onBack={handleBack} accent={accent} onAccentChange={setAccent} />

      <main className="main">
        {view === 'home' && (
          <WordSelector
            categories={wordCategories}
            activeCategory={activeCategory}
            onCategoryChange={setActiveCategory}
            onSelectWord={handleSelectWord}
          />
        )}

        {view === 'practice' && selectedWord && (
          <PracticeView
            word={selectedWord}
            accent={accent}
            onResult={handleResult}
            onError={handleError}
          />
        )}

        {view === 'results' && result && (
          <ResultsView
            result={result}
            word={selectedWord}
            onTryAgain={handleTryAgain}
            onNextWord={handleNextWord}
          />
        )}

        {view === 'error' && (
          <div className="practice" style={{ animation: 'fadeSlideUp 0.4s var(--ease-out)' }}>
            <div className="error-card">
              <div className="error-card__icon">⚠️</div>
              <div className="error-card__title">Something went wrong</div>
              <div className="error-card__message">{error}</div>
              <div className="actions">
                <button className="btn btn--secondary" onClick={handleBack}>
                  ← Go Home
                </button>
                <button className="btn btn--primary" onClick={handleTryAgain}>
                  🔄 Try Again
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
