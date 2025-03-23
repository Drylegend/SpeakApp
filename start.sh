#!/bin/bash
# Start the FastAPI backend (Uvicorn) in the background, binding to localhost.
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
# Start Nginx in the foreground.
nginx -g 'daemon off;'
