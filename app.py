# app.py
from modules.download import download_audio
from modules.transcription import transcribe_audio
from modules.extraction import extract_exercises_from_transcript
import os
import ssl

def main():
    # Set SSL context to use certifi's certificate bundle
    ssl._create_default_https_context = ssl._create_unverified_context

    # Ensure the audio output directory exists
    os.makedirs("yt_video_audio", exist_ok=True)
    
    # Get the YouTube video URL from the user
    video_url = input("Enter the YouTube video URL: ")
    
    try:
        # Step 1: Download audio from YouTube
        audio_path = download_audio(video_url)
        
        # Display success message with the downloaded audio path
        print(f"\tAudio downloaded successfully at:\n\t {audio_path}\n")

        #Step 2: Get the transcript for the yt video
        transcript_path = transcribe_audio(audio_path)

        # Display success message with the downloaded transcript path
        print(f"\tTranscript successfully generated at:\n\t {transcript_path}\n")

        #Step 2: Get the transcript for the yt video
        exersises_path = extract_exercises_from_transcript(transcript_path)

        # Display success message with the downloaded transcript path
        print(f"\tSuccesfully extracted the routine from the video at -- \n\t {exersises_path}\n")
    
    except ValueError as e:
        # Display error message if download fails
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
