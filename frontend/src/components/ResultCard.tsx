import type { Prediction } from "../api";

export function ResultCard({ prediction }: { prediction: Prediction }) {
  const percent = Math.round(prediction.confidence * 100);
  const kind = prediction.is_hotdog ? "yes" : "no";

  return (
    <div className={`result result--${kind}`}>
      <span className="result__label">{prediction.label}</span>
      <div className="result__bar">
        <div className="result__fill" style={{ width: `${percent}%` }} />
      </div>
      <span className="result__confidence">{percent}% confident</span>
    </div>
  );
}
