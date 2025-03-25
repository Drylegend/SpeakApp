# -------- Stage 1: Build Frontend --------
    FROM node:18 AS frontend-builder
    WORKDIR /app/frontend
    # Copy package.json and yarn.lock for dependency caching
    COPY frontend/package.json frontend/yarn.lock ./
    # Install dependencies using Yarn with exact versions
    RUN yarn --exact
    # (Optional) Initialize Tailwind if needed
    RUN npx tailwindcss init -p
    # Copy the rest of the frontend source code
    COPY frontend/ ./
    # Build the production assets (Vite outputs to the "dist" folder)
    RUN yarn build
    
    # -------- Stage 2: Build Backend --------
    FROM python:3.11-bullseye AS backend-builder
    WORKDIR /app/backend
    # Install system dependencies required for audio processing
    RUN apt-get update && \
        apt-get install -y --no-install-recommends ffmpeg libsndfile1 && \
        rm -rf /var/lib/apt/lists/*
    # Copy requirements.txt and install Python dependencies globally
    COPY requirements.txt .
    RUN pip install --prefer-binary --no-cache-dir -r requirements.txt
    # Copy backend source code
    COPY backend/ .
    
    # -------- Stage 3: Prebuilt FFmpeg --------
    FROM jrottenberg/ffmpeg:4.4-ubuntu AS ffmpeg-builder
    # This stage uses an image with FFmpeg preinstalled.
    # No additional commands are needed.
    
    # -------- Stage 4: Final Production Image --------
    FROM python:3.11-bullseye AS final
    WORKDIR /app
    # Install system dependency for audio processing (libsndfile1)
    RUN apt-get update && \
        apt-get install -y --no-install-recommends libsndfile1 && \
        rm -rf /var/lib/apt/lists/*
    # Copy prebuilt FFmpeg binary from the ffmpeg-builder stage (located at /usr/local/bin)
    COPY --from=ffmpeg-builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
    # Copy built backend from the backend-builder stage
    COPY --from=backend-builder /app/backend /app/backend
    # Copy built frontend assets from the frontend-builder stage
    COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
    # Expose port 8000 for Uvicorn
    EXPOSE 8000
    # Set the default command to run Uvicorn serving your FastAPI app on port 8000.
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    
