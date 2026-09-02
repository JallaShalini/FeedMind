import React from 'react'

const cards = [
  { key: 'total', label: 'Total Feedback', color: 'accent' },
  { key: 'positive', label: 'Positive', color: 'accent-green' },
  { key: 'negative', label: 'Negative', color: 'accent-red' },
  { key: 'neutral', label: 'Neutral', color: 'glass' },
]

export default function MetricsCards({ summary }) {
  const total = summary?.total || 1; // prevent division by zero
  
  return (
    <section className="metrics-grid">
      {cards.map((card) => {
        const val = summary?.[card.key] ?? 0;
        const percent = card.key !== 'total' ? Math.round((val / total) * 100) : null;
        
        return (
          <article key={card.key} className={`metric-card ${card.color} glass`}>
            <span>{card.label}</span>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
              <strong>{val}</strong>
              {percent !== null && (
                <small style={{ color: 'var(--muted)', fontSize: '1rem', fontWeight: '500' }}>
                  {percent}%
                </small>
              )}
            </div>
          </article>
        )
      })}
    </section>
  )
}
