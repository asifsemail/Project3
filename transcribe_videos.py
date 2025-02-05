"""
# Video Transcription Module

This module handles the audio extraction and transcription of YouTube videos using Whisper AI.

## Summary
- Downloads audio from YouTube videos using yt-dlp
- Transcribes audio using OpenAI's Whisper model
- Saves transcriptions as text files
- Handles various YouTube URL formats
- Provides error handling for failed downloads/transcriptions

## Dependencies

### System Requirements
1. **FFmpeg**
   - Windows: Install via chocolatey `choco install ffmpeg`
   - Mac: Install via homebrew `brew install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`
2. Python 3.8+
3. Sufficient disk space for temporary audio files

### Package Dependencies
1. **openai-whisper==20231106**
   - Install: `pip install openai-whisper`
   - Purpose: Audio transcription
   
2. **yt-dlp==2023.11.16**
   - Install: `pip install yt-dlp`
   - Purpose: YouTube audio downloading
   
3. **torch**
   - Install: `pip install torch`
   - Purpose: Required by Whisper for model operations

### Project Dependencies
1. **output/** directory
   - Must exist or have permissions to create
   - Stores transcription text files

## Functions
1. extract_video_id(url)
   - Extracts YouTube video ID from various URL formats
   - Handles both youtube.com and youtu.be URLs
   
2. transcribe_and_save(url, output_dir="output")
   - Downloads audio
   - Performs transcription
   - Saves result to file
   - Returns file path and transcription text

## Returns
Dictionary containing:
- file_path: Path to saved transcription
- transcription: Full transcription text
- error: Error message if transcription fails

## Error Handling
- Returns error dictionary if:
  - Video URL is invalid
  - Audio download fails
  - Transcription fails
  - File writing fails
"""


# import dependencies
import whisper
import yt_dlp
import os

# Load Whisper model
MODEL = whisper.load_model("base")
# MODEL = whisper.load_model("base", weights_only=True)

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
        result = MODEL.transcribe(audio_url)
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

