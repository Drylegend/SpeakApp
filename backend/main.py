# uvicorn main:app
# uvicorn main:app --reload
# venv\Scripts\activate
# uvicorn main:app --reload --host 0.0.0.0 --port 8000

import os
import time
import subprocess
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import librosa
from faster_whisper import WhisperModel
import google.generativeai as genai

# Import your functions
from functions.open_requests import get_chat_response, reset_messages
from functions.rag_agent import generate_rag_response  # Ensure generate_rag_response lazily calls init_rag() if needed

app = FastAPI()

# Base directory (directory of this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define relative paths for models and executables
FAST_WHISPER_DIR = os.path.join(BASE_DIR, "models", "fast_whisper")
PIPER_DIR = os.path.join(BASE_DIR, "models", "piper")
PIPER_EXE = os.path.join(PIPER_DIR, "piper.exe")
JENNY_MODEL_PATH = os.path.join(PIPER_DIR, "en_GB-jenny_dioco-medium.onnx")

# Download models from Google Drive before anything else
from download_models import download_and_extract_models
download_and_extract_models()

# (Do not call init_rag() here so that the heavy RAG system is only loaded if needed)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy initialization for the Fast Whisper model
whisper_model = None
model_size = "tiny"

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        logger.info("Loading Fast Whisper model...")
        whisper_model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            download_root=FAST_WHISPER_DIR
        )
    return whisper_model

def text_to_speech_jenny(text, filename):
    subprocess.run(
        [PIPER_EXE, "-m", JENNY_MODEL_PATH, "-f", filename],
        input=text.encode("utf-8")
    )

@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    try:
        # Ensure upload directory exists
        upload_dir = os.path.join(BASE_DIR, "uploaded_audio")
        os.makedirs(upload_dir, exist_ok=True)
        file_location = os.path.join(upload_dir, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        # Load audio using librosa
        speech_array, sampling_rate = librosa.load(file_location, sr=16000)
        
        # Transcription using lazy-loaded Fast Whisper model
        start_time = time.time()
        model_inst = get_whisper_model()
        segments, info = model_inst.transcribe(file_location, language="en")
        end_time = time.time()
        transcription = " ".join([segment.text for segment in segments])
        logger.info(f"Fast Whisper Transcription: {transcription}")
        logger.info(f"Transcription Time: {end_time - start_time} seconds")
        
        # Determine response using RAG or standard chat based on transcription
        try:
            if "reva" in transcription.lower():
                # generate_rag_response should internally check if RAG is initialized and call init_rag() if not.
                chat_response = generate_rag_response(transcription)
            else:
                chat_response = get_chat_response(transcription)
            logger.info(f"Chat Response: {chat_response}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")
        
        # Convert text response to speech using Piper
        try:
            response_audio_file = os.path.join(BASE_DIR, "response_audio.wav")
            text_to_speech_jenny(chat_response, response_audio_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")
        
        # Stream the audio file as response
        def iterfile():
            with open(response_audio_file, "rb") as file_like:
                yield from file_like
        
        return StreamingResponse(iterfile(), media_type="audio/wav")
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"error": "An internal server error occurred.", "details": str(e)}

@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation Reset"}
