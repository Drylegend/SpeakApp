# 🧠 SpeakAI: Intelligent Voice Assistant

A real-time AI-powered voice assistant that listens, understands, and responds with human-like speech.

SpeakAI is a fast, efficient, and offline-capable voice assistant built using modern speech recognition, RAG-based text generation, and lightweight text-to-speech models. It processes user speech locally, generates intelligent responses, and speaks back in real time — all without cloud dependency.

# 🚀 Overview

SpeakAI is designed as a production-oriented, modular system combining:

Speech-to-Text (STT) for converting user audio to text

AI Response Generation through a lightweight RAG model and LLM API

Text-to-Speech (TTS) for generating natural, low-latency audio

Local Deployment using FastAPI + Nginx reverse proxy

Docker-based packaging for reproducible production setups

Frontend UI built with React.js for seamless interaction

The entire system is architected for real-time performance (< 6s response time), portable deployment (including local machines), and multi-language extensibility.

# ⚙️ System Architecture
```
User Speaks → Whisper STT → RAG Retriever → LLM Agent → AI Response → Piper TTS → Audio Output
```

# 🎯 Key Features

⚡ Real-time Speech Processing (Whisper)

🤖 AI-Powered Responses (Gemini API / any pluggable LLM)

🌍 Multi-language capability (extendable)

🔍 Retrieval-Augmented Generation (RAG) using CSV/vector embeddings

🚀 Fast Performance — optimized pipeline with < 6 seconds latency

🖥️ Fully Local Deployment — no cloud dependency required

🧩 Modular Architecture — interchangeable STT, TTS, and LLM models

🔒 Production-ready setup with Nginx + Docker

# 🛠️ Tech Stack
Backend & AI Processing

FastAPI — API server

Whisper — Speech-to-Text

Piper TTS — Text-to-Speech

Gemini API / LLMs — Response generation

RAG Engine — Context retrieval using embeddings

MongoDB — Data storage (optional)

Frontend

React.js — User interface

Tailwind CSS — Component styling

Deployment

Nginx — Reverse proxy and static asset serving

Docker / Docker Compose — Containerized build

start.sh — Automated startup script (venv creation + Nginx + FastAPI)

📦 Project Structure
```
speakai/
│── backend/
│   ├── app.py
│   ├── rag_engine.py
│   ├── requirements.txt
│   ├── start.sh
│   ├── Dockerfile
│── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│── nginx/
│   ├── nginx.conf
│── embeddings/
│── README.md
```
# 🐳 Docker Deployment Overview
Dockerfile (Backend)

A generalised example:

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["bash", "start.sh"]

start.sh (auto-venv + server bootstrap)
#!/bin/bash

# Create virtual environment if missing
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000

🌐 Reverse Proxy (Nginx)

Basic configuration:

server {
    listen 80;

    location /api/ {
        proxy_pass http://backend:8000/;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}

🧪 How It Works (Pipeline Flow)

User speaks into the microphone

Whisper transcribes speech → text

RAG engine extracts context from CSV embeddings

LLM (Gemini API or local model) generates response

Piper TTS converts response text → speech audio

Frontend plays audio instantly

📈 Performance

End-to-end response time: < 6 seconds

Whisper + Piper TTS provide fast offline inference

Nginx ensures quick static delivery + load balancing

🧩 Future Enhancements

Add GPU acceleration

Add multi-user session manager

Implement on-device vector store

Add mobile UI (React Native)

👨‍💻 Author

Utsav Chatterjee (AI & DS)
REVA University

🔗 Source Code

👉 GitHub Repository: https://github.com/Drylegend/SpeakApp

