

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg
# Copy the requirements file (adjust path if needed)
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container
COPY backend/ ./backend/

# Copy the download_models.py file from backend into the container root
COPY backend/download_models.py ./

# Expose the port that your app listens on
EXPOSE 8000


WORKDIR /app/backend

# Set the command to run your app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
