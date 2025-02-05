"""
# Command Line Interface Module

This module provides a CLI alternative to the Gradio web interface for the VidInsight AI application.

## Summary
- Offers command-line interaction for video analysis
- Provides sequential processing of videos
- Displays results directly in the terminal
- Serves as a debugging and testing tool

## Dependencies

### System Requirements
- Python 3.8+
- Internet connection for API calls
- FFmpeg for audio processing

### Package Dependencies
No additional package installations required beyond project dependencies

### Project Dependencies
1. **Local Modules**
   - fetch_youtube_videos.py: For YouTube video retrieval
   - transcribe_videos.py: For video transcription

## Functions
main()
- Gets user input for topic
- Coordinates video fetching and transcription
- Displays results in terminal format

## Usage Example
python main.py
Enter topic to analyze: Machine Learning

## Returns
Terminal output containing:
1. Video Information
   - Title
   - URL
2. Transcription Status
   - Success/failure messages
   - Transcription text or error

## Error Handling
- Video fetching errors
- Transcription failures
- Invalid input handling

"""


from fetch_youtube_videos import fetch_videos
from transcribe_videos import transcribe

def main():
    topic = input("Enter topic to analyze: ")
    print("\nFetching videos...")
    
    videos = fetch_videos(topic)
    if isinstance(videos, str):
        print(f"Error: {videos}")
        return
    
    for idx, video in enumerate(videos, 1):
        print(f"\nVideo {idx}: {video['title']}")
        print(f"URL: {video['url']}")
        print("Transcribing...")
        print(transcribe(video['url']))

if __name__ == "__main__":
    main()
