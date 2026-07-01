"""FastAPI service for the hotdog / not-hotdog classifier.

Exposes POST /classify, which takes an uploaded image and returns the prediction as JSON.
Interactive docs are auto-generated at /docs.
"""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from classifier import classify

app = FastAPI(title="Not Hotdog API", version="1.0.0")

# Allow the React dev server to call the API from the browser (relaxed for local dev).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict:
    """Simple health check so we can confirm the service is up."""
    return {"status": "ok"}


@app.post("/classify")
async def classify_image(file: UploadFile = File(...)) -> dict:
    # reject anything that isn't an image
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    return classify(image_bytes)
