const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Prediction {
  label: string;
  is_hotdog: boolean;
  confidence: number;
}

export async function classifyImage(file: File): Promise<Prediction> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_URL}/classify`, { method: "POST", body: form });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? "Failed to classify image.");
  }
  return res.json();
}
