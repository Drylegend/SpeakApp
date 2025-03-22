# uvicorn main:app
# uvicorn main:app --reload
# venv\Scripts\activate
# uvicorn main:app --reload --host 0.0.0.0 --port 8000

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import librosa
import time
from faster_whisper import WhisperModel
import subprocess
import logging
import google.generativeai as genai

# Import your functions
from functions.open_requests import get_chat_response, reset_messages
from functions.rag_agent import init_rag, generate_rag_response

app = FastAPI()

# Initialize the RAG system on startup
init_rag()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Fast Whisper model from the specified directory
model_dir = "E:/SpeakAI/backend/models/fast_whisper/"
model_size = "tiny"
model = WhisperModel(model_size, device="cpu", compute_type="int8", download_root=model_dir)

def text_to_speech_jenny(text, filename):
    model_path = "E:/SpeakAI/backend/models/piper/en_GB-jenny_dioco-medium.onnx"
    subprocess.run([
        "E:/SpeakAI/backend/models/piper/piper.exe",
        "-m", model_path,
        "-f", filename
    ], input=text.encode('utf-8'))

@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_location = f"uploaded_audio/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Load audio using librosa
        speech_array, sampling_rate = librosa.load(file_location, sr=16000)

        # Measure transcription time
        start_time = time.time()
        segments, info = model.transcribe(file_location, language="en")
        end_time = time.time()

        # Concatenate transcribed segments
        transcription = " ".join([segment.text for segment in segments])
        logger.info(f"Fast Whisper Transcription: {transcription}")
        logger.info(f"Transcription Time: {end_time - start_time} seconds")

        # ---------------------------------------------------------
        # Decide if it's about REVA, then pick the right approach
        # ---------------------------------------------------------
        try:
            if "reva" in transcription.lower():
                chat_response = generate_rag_response(transcription)
            else:
                chat_response = get_chat_response(transcription)

            logger.info(f"Chat Response: {chat_response}")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")

        # Text-to-speech conversion with Piper
        try:
            response_audio_file = "response_audio.wav"
            text_to_speech_jenny(chat_response, response_audio_file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")

        def iterfile():
            with open(response_audio_file, mode="rb") as file_like:
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
