# modules/download.py
import os
from pytubefix import YouTube

def download_audio(video_url: str, output_dir: str = "yt_video_audio") -> str:
    try:
        # Create a YouTube object using the provided video URL
        yt = YouTube(video_url)
        
        # Extract the video title and channel name
        video_title = yt.title.replace(" ", "_").replace("/", "_").lower()
        channel_name = yt.author.replace(" ", "_").replace("/", "_").upper()
        
        # Combine the video title and channel name to create a unique filename
        unique_filename = f"{channel_name}_{video_title}.mp4"
        
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the path for the audio file
        audio_path = os.path.join(output_dir, unique_filename)
        
        # Download the audio stream and save it in the specified directory with the new name
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=output_dir, filename=unique_filename)
        
        # Return the path of the downloaded audio file
        return audio_path
    
    # Handle any exception that occurs during download and raise a descriptive error
    except Exception as e:
        raise ValueError(f"Failed to download video: {e}")
