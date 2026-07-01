"""FastAPI service for the hotdog / not-hotdog classifier.

Exposes POST /classify (upload an image -> JSON prediction) and GET /health. In production
it also serves the built React frontend from the same origin, so the whole app runs behind
a single URL. Interactive API docs are at /docs.
"""

import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from classifier import classify

app = FastAPI(title="Not Hotdog API", version="1.0.0")

# Relaxed CORS for local dev where the frontend runs on a different port. In the single-URL
# deploy the frontend is same-origin, so this is a no-op there.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/classify")
async def classify_image(file: UploadFile = File(...)) -> dict:
    # Reject anything that isn't an image before we waste time decoding it.
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    return classify(image_bytes)


# Serve the built React app if it's present (production/Docker). Mounted last so it doesn't
# shadow the API routes above. Absent in local dev, where Vite serves the frontend instead.
FRONTEND_DIR = Path(os.getenv("FRONTEND_DIR", Path(__file__).resolve().parent.parent / "frontend" / "dist"))
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
