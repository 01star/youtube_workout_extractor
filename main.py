# app.py
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from modules.download import download_audio
from modules.transcription import transcribe_audio
from modules.extraction import extract_exercises_from_transcript
import os
import ssl

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# Home route - Display the workout form
@app.get("/", response_class=HTMLResponse)
async def get_workout_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle manual workout input
@app.post("/manual_workout", response_class=HTMLResponse)
async def manual_workout(
    request: Request,
    exercise: str = Form(...),
    sets: int = Form(...),
    reps: int = Form(...)
):
    # Here you can store the workout data in a list or database (currently showing it back to the user)
    workout = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps
    }

    # Render the result on a new page
    return templates.TemplateResponse("result.html", {"request": request, "workout": workout})

# Route to handle YouTube video link and extract workout
@app.post("/extract_workout", response_class=HTMLResponse)
async def extract_workout(
    request: Request,
    youtube_url: str = Form(...)
):
    # # Set SSL context to use certifi's certificate bundle
    # ssl._create_default_https_context = ssl._create_unverified_context

    # # Ensure the audio output directory exists
    # os.makedirs("yt_video_audio", exist_ok=True)
    
    # Get the YouTube video URL from the user
    # video_url = input("Enter the YouTube video URL: ")
    
    try:
        # Step 1: Download audio from YouTube
        audio_path = download_audio(youtube_url)
        
        # Display success message with the downloaded audio path
        print(f"\tAudio downloaded successfully at:\n\t {audio_path}\n")

        #Step 2: Get the transcript for the yt video
        transcript_path = transcribe_audio(audio_path)

        # Display success message with the downloaded transcript path
        print(f"\tTranscript successfully generated at:\n\t {transcript_path}\n")

        #Step 2: Get the transcript for the yt video
        routine_path = extract_exercises_from_transcript(transcript_path)

        # Display success message with the downloaded transcript path
        print(f"\tSuccesfully extracted the routine from the video at -- \n\t {routine_path}\n")

        # Read the generated workout routine
        with open(routine_path, "r") as file:
            workout_routine = file.read()

        # Render the result on a new page
        return templates.TemplateResponse("result.html", {"request": request, "workout": workout_routine})

    except ValueError as e:
        return templates.TemplateResponse("result.html", {"request": request, "error": str(e)})
