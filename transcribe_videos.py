"""
This module is responsible for downloading audio from YouTube videos, transcribing the audio into text, 
and saving the transcriptions to an output folder. It uses OpenAI's Whisper model for transcription 
and yt-dlp for downloading audio.

## Overview
This module performs the following tasks:
1. Extracts the video ID from a given YouTube URL.
2. Downloads the audio from the video using yt-dlp.
3. Transcribes the audio into text using OpenAI's Whisper model.
4. Saves the transcription to a `.txt` file in the specified output directory.

## Dependencies
1. **yt-dlp**: For downloading audio from YouTube videos.
   - Install via: `pip install yt-dlp`
2. **OpenAI Whisper**: For transcribing audio into text.
   - Install via: `pip install openai-whisper`
3. **os**: For file and directory operations.

"""

# import dependencies
import whisper
import yt_dlp
import os

# Load Whisper model
MODEL = whisper.load_model("base")

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Args:
        url (str): YouTube video URL.
    Returns:
        str: Video ID.
    """
    if "v=" in url:
        return url.split("v=")[-1]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1]
    return "unknown_video_id"

def transcribe_and_save(url, output_dir="output"):
    """
    Transcribe audio from a YouTube video and save it to a file.
    Args:
        url (str): YouTube video URL.
        output_dir (str): Directory to save the transcription.
    Returns:
        dict: Contains the file path and transcription text.
    """
    try:
        # Download audio with yt-dlp
        with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
        
        # Transcribe audio
        result = MODEL.transcribe(audio_url, fp16=False)
        transcription = result['text']

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Use video ID as file name
        video_id = extract_video_id(url)
        file_path = os.path.join(output_dir, f"{video_id}.txt")
        
        # Save transcription to a file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcription)

        return {"file_path": file_path, "transcription": transcription}

    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}

