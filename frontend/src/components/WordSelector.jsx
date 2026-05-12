export default function WordSelector({ categories, activeCategory, onCategoryChange, onSelectWord }) {
  const activeCat = categories.find(c => c.id === activeCategory) || categories[0];

  return (
    <div>
      {/* Welcome section */}
      <div className="welcome">
        <div className="welcome__emoji">🗣️</div>
        <h1 className="welcome__title">Practice Your Pronunciation</h1>
        <p className="welcome__desc">
          Choose a word or sentence, record your voice, and get instant AI-powered feedback with detailed scoring.
        </p>
      </div>

      {/* Category Tabs */}
      <div className="category-tabs" role="tablist">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`category-tab ${activeCategory === cat.id ? 'category-tab--active' : ''}`}
            onClick={() => onCategoryChange(cat.id)}
            role="tab"
            aria-selected={activeCategory === cat.id}
          >
            <span>{cat.icon}</span>
            <span>{cat.title}</span>
          </button>
        ))}
      </div>

      {/* Word Cards */}
      <div className="word-list" key={activeCategory}>
        {activeCat.items.map((item, i) => (
          <button
            key={item.text}
            className="word-card"
            onClick={() => onSelectWord(item)}
            style={{ animationDelay: `${i * 0.05}s` }}
          >
            <div>
              <div className="word-card__text">{item.display}</div>
              {item.phonemeHint && (
                <div className="word-card__hint">{item.phonemeHint}</div>
              )}
            </div>
            <span className="word-card__arrow">→</span>
          </button>
        ))}
      </div>
    </div>
  );
}
