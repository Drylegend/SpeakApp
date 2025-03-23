# -------- Stage 1: Build Frontend --------
FROM node:16 AS frontend-builder
WORKDIR /app/frontend
# Copy frontend package files and install dependencies
COPY frontend/package*.json ./
RUN npm install
# Copy entire frontend source and build the production assets
COPY frontend/ .
RUN npm run build

# -------- Stage 2: Build Backend --------
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend
# Install system dependencies (ffmpeg and libsndfile for audio processing)
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# Copy backend source code
COPY backend/ .

# -------- Stage 3: Final Production Image --------
FROM python:3.11-slim
WORKDIR /app
# Install system dependencies, Nginx, and Supervisor (for managing processes)
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 nginx supervisor

# Copy built backend and frontend from previous stages
COPY --from=backend-builder /app/backend /app/backend
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy configuration files for Nginx and the startup script
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port 80 for the container (Nginx will listen on this port)
EXPOSE 80

# Set the default command to run the startup script
CMD ["/app/start.sh"]
