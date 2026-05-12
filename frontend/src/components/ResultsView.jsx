import { useEffect, useState, useMemo } from 'react';

export default function ResultsView({ result, word, onTryAgain, onNextWord }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  const score = result?.score ?? 0;

  // Animate score count-up
  useEffect(() => {
    setAnimatedScore(0);
    const duration = 1200;
    const start = performance.now();

    const animate = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out curve
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.round(eased * score));
      if (progress < 1) requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
  }, [score]);

  // Score grade
  const grade = useMemo(() => {
    if (score >= 90) return { text: '🌟 Excellent!', class: 'excellent' };
    if (score >= 70) return { text: '👍 Good Job!', class: 'good' };
    if (score >= 50) return { text: '💪 Keep Practicing', class: 'fair' };
    return { text: '📚 Needs Work', class: 'poor' };
  }, [score]);

  // Score color
  const scoreColor = useMemo(() => {
    if (score >= 90) return '#22c55e';
    if (score >= 70) return '#3b82f6';
    if (score >= 50) return '#eab308';
    return '#ef4444';
  }, [score]);

  // SVG circle values
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedScore / 100) * circumference;

  // Phoneme comparison data
  const comparison = result?.comparison || [];

  // Feedback with icons
  const feedbackItems = (result?.feedback || []).map((msg, i) => {
    let type = 'info';
    let icon = 'ℹ️';
    if (msg.includes('Good') || msg.includes('Excellent') || msg.includes('Perfect')) {
      type = 'success'; icon = '✅';
    } else if (msg.includes('not clear') || msg.includes('wrong')) {
      type = 'error'; icon = '❌';
    } else if (msg.includes('missed') || msg.includes('missing')) {
      type = 'warning'; icon = '⚠️';
    } else if (msg.includes('Extra')) {
      type = 'warning'; icon = '➕';
    }
    return { msg, type, icon, id: i };
  });

  // Deduplicate feedback
  const uniqueFeedback = feedbackItems.filter(
    (item, i, arr) => arr.findIndex(x => x.msg === item.msg) === i
  );

  return (
    <div className="results">
      {/* Score Circle */}
      <div className="score-section">
        <div className="score-circle">
          <svg className="score-circle__svg" viewBox="0 0 160 160">
            <circle className="score-circle__track" cx="80" cy="80" r={radius} />
            <circle
              className="score-circle__fill"
              cx="80" cy="80" r={radius}
              stroke={scoreColor}
              strokeDasharray={circumference}
              strokeDashoffset={offset}
            />
          </svg>
          <div className="score-circle__value">
            <div className="score-circle__number" style={{ color: scoreColor }}>
              {animatedScore}
            </div>
            <div className="score-circle__label">Score</div>
          </div>
        </div>
        <div className={`score-grade score-grade--${grade.class}`}>
          {grade.text}
        </div>
      </div>

      {/* Phoneme Breakdown */}
      {comparison.length > 0 && (
        <div className="phoneme-section">
          <div className="section-title">
            🔤 Phoneme Breakdown
          </div>
          <div className="phoneme-grid">
            {comparison.map((p, i) => (
              <div
                key={i}
                className={`phoneme-pill phoneme-pill--${p.type}`}
                style={{ animationDelay: `${i * 0.06}s` }}
                title={getTooltip(p)}
              >
                <span className="phoneme-pill__icon">
                  {p.type === 'correct' ? '✓' : p.type === 'wrong' ? '✗' : p.type === 'missing' ? '?' : '+'}
                </span>
                <span>{p.spoken || p.expected || '—'}</span>
                {p.type === 'wrong' && p.expected && (
                  <span className="phoneme-pill__expected">{p.expected}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feedback */}
      <div className="feedback-section">
        <div className="section-title">💬 Feedback & Corrections</div>
        <div className="feedback-list">
          {uniqueFeedback.map((item, i) => (
            <div
              key={item.id}
              className={`feedback-item feedback-item--${item.type}`}
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <span className="feedback-item__icon">{item.icon}</span>
              <span>{item.msg}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Correction Tips */}
      {comparison.some(p => p.type !== 'correct') && (
        <div className="feedback-section">
          <div className="section-title">🎯 How to Improve</div>
          <div className="feedback-list">
            {comparison
              .filter(p => p.type !== 'correct')
              .slice(0, 5)
              .map((p, i) => (
                <div
                  key={i}
                  className="feedback-item feedback-item--info"
                  style={{ animationDelay: `${i * 0.1}s` }}
                >
                  <span className="feedback-item__icon">💡</span>
                  <span>{getCorrectionTip(p)}</span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="actions">
        <button className="btn btn--secondary" onClick={onTryAgain}>
          🔄 Try Again
        </button>
        <button className="btn btn--primary" onClick={onNextWord}>
          Next Word →
        </button>
      </div>
    </div>
  );
}

function getTooltip(p) {
  switch (p.type) {
    case 'correct': return `Correct: "${p.spoken}"`;
    case 'wrong': return `Expected "${p.expected}" but heard "${p.spoken}"`;
    case 'missing': return `Missing sound: "${p.expected}"`;
    case 'extra': return `Extra sound detected: "${p.spoken}"`;
    default: return '';
  }
}

function getCorrectionTip(p) {
  switch (p.type) {
    case 'wrong':
      return `You said "${p.spoken}" — try pronouncing "${p.expected}" more clearly`;
    case 'missing':
      return `You missed the "${p.expected}" sound — make sure to include it`;
    case 'extra':
      return `Extra "${p.spoken}" sound detected — try to avoid adding it`;
    default:
      return 'Keep practicing!';
  }
}
