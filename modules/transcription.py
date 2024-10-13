# modules/extraction.py
import os
import whisper
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def transcribe_audio(audio_path: str, output_dir: str = "yt_audio_transcription") -> str:
    try:
        # Load the Whisper model (using the 'tiny' version for lightweight processing)
        model = whisper.load_model("tiny")
        
        # Transcribe the audio file
        result = model.transcribe(audio_path)
        transcript = result["text"]
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a filename for the transcription file based on the audio file name
        base_filename = os.path.splitext(os.path.basename(audio_path))[0]
        transcription_filename = f"{base_filename}_transcript.txt"
        transcription_path = os.path.join(output_dir, transcription_filename)
        
        # Save the transcription to the specified directory
        with open(transcription_path, "w") as f:
            f.write(transcript)
        
        # Return the path of the saved transcription file
        return transcription_path
    
    # Handle any exception that occurs during transcription and raise a descriptive error
    except Exception as e:
        raise ValueError(f"Failed to transcribe audio: {e}")