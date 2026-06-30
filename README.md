# 🌭 Not Hotdog — ML Image Processor

> Inspired by the "SeeFood" app from HBO's *Silicon Valley*. Upload an image and the app
> tells you whether it's a **Hotdog 🌭** or **Not Hotdog ❌**, with a confidence score.

A full-stack machine learning project built to be **readable and educational** — every
component is documented to explain *why* each decision was made, not just *what* it does.

This README grows step by step as the project is built (see the checklist below).

---

## What it does

1. You upload or drag-and-drop an image in the browser.
2. A FastAPI backend runs it through a trained **Convolutional Neural Network (CNN)**.
3. You get back a label (`Hotdog` / `Not Hotdog`) and a confidence percentage.

**Stack:** TensorFlow/Keras (model) · FastAPI (API) · React + TypeScript (frontend) · Docker.

---

## Build steps

- [x] **1. Project structure + README skeleton**
- [ ] **2. Data pipeline** — folder structure + Kaggle dataset download instructions
- [ ] **3. Image preprocessing** — resize to 224×224, normalize, data augmentation
- [ ] **4. CNN model architecture** — Conv2D, MaxPooling2D, Dense, binary crossentropy
- [ ] **5. Training script** — early stopping + model checkpoint callbacks
- [ ] **6. Evaluation** — accuracy, loss curves, confusion matrix
- [ ] **7. Save model** for deployment (`.h5`)
- [ ] **8. FastAPI backend** — `POST /classify` endpoint
- [ ] **9. Rate limiting** with slowapi — 10 requests/min/IP
- [ ] **10. React frontend** — drag-and-drop upload + confidence display
- [ ] **11. Docker + docker-compose** — containerize everything
- [ ] **12. Final README** — full documentation, architecture diagram, design decisions

---

## License

For educational purposes. The dataset is subject to its own license on Kaggle.
