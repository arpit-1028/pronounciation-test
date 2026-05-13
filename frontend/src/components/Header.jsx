export default function Header({ view, onBack, accent, onAccentChange }) {
  return (
    <header className="header">
      <div className="header__brand">
        <div className="header__icon">🎙️</div>
        <div>
          <div className="header__title">Speech Coach</div>
          <div className="header__subtitle">AI Pronunciation Trainer</div>
        </div>
      </div>

      <div className="header__actions">
        {/* Accent Selector */}
        <div className="accent-selector">
          <select
            className="accent-select"
            value={accent}
            onChange={(e) => onAccentChange(e.target.value)}
            aria-label="Accent mode"
          >
            <option value="auto">🌐 Auto Detect</option>
            <option value="indian">🇮🇳 Indian English</option>
            <option value="british">🇬🇧 British English</option>
          </select>
        </div>

        {view !== 'home' && (
          <button className="header__back" onClick={onBack}>
            ← Back
          </button>
        )}
      </div>
    </header>
  );
}
