# Single-image build for Hugging Face Spaces: builds the React frontend, then runs the
# FastAPI API which serves both the /classify endpoint and the static frontend on one port.

FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
# Empty API URL -> the app calls /classify on the same origin (no CORS, one URL).
ENV VITE_API_URL=""
RUN npm run build

# ---- Python ----
FROM python:3.11-slim
WORKDIR /app/api

# Match the training stack so the saved Keras 2 model loads cleanly. tensorflow-cpu keeps
# the image small (no CUDA) since inference runs on CPU.
ENV TF_USE_LEGACY_KERAS=1
RUN pip install --no-cache-dir \
    "fastapi>=0.110" "uvicorn[standard]>=0.29" "python-multipart>=0.0.9" \
    "pillow>=10.0" "numpy<2.0" "tf-keras" "tensorflow-cpu==2.16.2"

COPY api/ /app/api/
COPY model/hotdog_classifier.h5 /app/model/hotdog_classifier.h5
COPY --from=frontend /frontend/dist /app/frontend/dist

# Hugging Face Spaces routes to port 7860 by default.
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
