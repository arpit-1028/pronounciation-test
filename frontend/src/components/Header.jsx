import { useState, useEffect, useRef, useCallback } from 'react';

export default function Header({ view, onBack }) {
  return (
    <header className="header">
      <div className="header__brand">
        <div className="header__icon">🎙️</div>
        <div>
          <div className="header__title">Speech Coach</div>
          <div className="header__subtitle">AI Pronunciation Trainer</div>
        </div>
      </div>
      {view !== 'home' && (
        <button className="header__back" onClick={onBack}>
          ← Back
        </button>
      )}
    </header>
  );
}
