import { useState } from "react";

import { classifyImage, type Prediction } from "./api";
import { Dropzone } from "./components/Dropzone";
import { ResultCard } from "./components/ResultCard";

export default function App() {
  const [preview, setPreview] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    setPreview(URL.createObjectURL(file));
    setPrediction(null);
    setError(null);
    setLoading(true);
    try {
      setPrediction(await classifyImage(file));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <h1>ML Image Processor</h1>
      <p className="subtitle">Inspired by the "SeeFood" app from HBO's Silicon Valley. Upload an image and the app tells you whether it's a Hotdog or Not Hotdog, with a confidence score.</p>

      <Dropzone onFile={handleFile} disabled={loading} />

      {preview && <img className="preview" src={preview} alt="upload preview" />}
      {loading && <p className="status">Classifying…</p>}
      {error && <p className="status status--error">{error}</p>}
      {prediction && !loading && <ResultCard prediction={prediction} />}
    </main>
  );
}
