# VidInsight AI: AI-Powered YouTube Content Analyzer

## Overview
VidInsight AI is an AI-powered application designed to analyze YouTube videos for a given subject, extract insights, and provide transcriptions. The application is built to assist content creators, educators, researchers, and everyday users in understanding video content quickly and effectively.

---
This ReadMe file documents the current phase of the project and will be updated as new features are implemented.

**Current Features (Asif's Code):**

	1.	YouTube Video Retrieval:
    	•	Fetches up to 10 YouTube videos based on a user-provided topic.
    	•	Filters videos based on criteria such as keywords, view counts, and trusted channels.
    	•	Selects the top 3 videos based on relevance and view counts.
    
	2.	Transcription:
    	•	Transcribes audio from the top 3 selected videos using OpenAI’s Whisper model.
    	•	Saves the complete transcripts in an `output` folder for further processing.
    
	3.	User Interface:
    	•	Provides a user-friendly interface built with Gradio.
    	•	Displays video details (title, channel, views) and a preview of the transcription.

**Current Features (Kade's Code):**

	1.	Transcription Retrieval:
    	•	Reads all .txt files from the Output directory containing transcriptions.
        •	Stores transcription content in a dictionary for processing.
    
	2.	Gemini Processing:
    	•	Loads the Gemini API key from an environment file.
      	•	Uses the Gemini model and specified prompt to generate summaries and key insights from the transcriptions.

	3.	Summary & Key Points output:
    	•	Extracts a topic title, summary, and key points from the transcriptions.
        •	Formats the output for easy readability.details (title, channel, views) and a preview of the transcription.

**Current Features (Amit's Code):**

**Current Features (Simran's Code):**

**Current Features (Jason's Code):**

---

## Project Structure

VidInsight-AI/\
├── app.py                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Gradio app for user interaction \
├── config.py                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Configuration file for API keys and filters\
├── fetch_youtube_videos.py   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Fetches and filters YouTube videos\
├── transcribe_videos.py      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Transcribes videos and saves transcripts\
├── main.py                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # CLI-based alternative to run the app\
├── keys1.env                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Environment variables (e.g., YouTube API key)\
├── output/                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Folder for saved transcripts\
&nbsp;&nbsp;&nbsp;├── <video_id>.txt        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Transcripts saved as text files


---

## Setup Instructions (need to be completed)

1. Prerequisites\
	•	Python 3.8 or higher\
	•	A YouTube Data API key (create one via Google Cloud Console)

2. Installation
	1.	Clone the repository:
      ```python
      git clone <repository_url>
      ```
   	2.	Install required dependencies:

   	3.	Set up your API key:
	•	Create a `.env` file or update `keys1.env` with your YouTube API key:
    ```python
    YOUTUBE_API_KEY="your_api_key_here"
    ```
   \
    
3. Running the Application
	•	To launch the Gradio app:
    ```python
    python app.py
    ```
---

## Usage

#### Gradio App
	1.	Enter a topic in the “Enter learning topic” field (e.g., “Machine Learning”).
	2.	Click “Submit” to fetch and analyze videos.
	3.	View results, including:
    	•	Video title, channel name, view count.
    	•	A preview of the transcription.
    	•	The path to the saved transcript file.
#### Output Folder
	•	Complete transcripts are saved in the `output/` folder as `.txt` files.
	•	File names are based on unique YouTube video IDs (e.g., `ukzFI9rgwfU.txt`).

---

## Configuration

The `config.py` file allows customization of filtering criteria:
```python
FILTER_CONFIG = {
    "videoDuration": "medium",  # Focus on videos between 4 and 20 minutes
    "order": "relevance",       # Sort by relevance
    "trusted_channels": {
        "Khan Academy": "UC4a-Gbdw7vOaccHmFo40b9g",
        "edX": "UCEBb1b_L6zDS3xTUrIALZOw",
        "Coursera": "UC58aowNEXHHnflR_5YTtP4g",
    },
    "teaching_keywords": {"tutorial", "lesson", "course", "how-to", "introduction", "basics"},
    "non_teaching_keywords": {"fun", "experiment", "joke", "prank", "vlog"},
    "max_results": 10,          # Maximum number of videos fetched from YouTube API
    "min_view_count": 10000     # Minimum view count for relevance
}
```

---

## Known Issues
	1.	If no results are found or an error occurs during video fetching, the app displays an error message in JSON format.
	2.	Ensure that valid topics are entered; overly broad or unrelated topics may not yield meaningful results.

---

## Planned Features
	1.	Summarization (Kade):
    	•	Extract key insights from transcriptions.
    	•	Provide concise summaries for each video.
        
	2.	Vector Database Integration (Amit):
    	•	Store transcriptions as vector embeddings for similarity-based querying.
        
	3.	Content Idea Generation (Simran):
    	•	Generate actionable content ideas optimized for SEO metadata.
    	•	Update the Gradio App based on the output       
        
	4.	Multilingual Support (Future):
    	•	Add support for transcription in other languages (e.g., Spanish, French).
        
	5.	Interactive Q&A (Future):
    	•	Allow users to ask questions about analyzed video content.

---

## Technology Stack

| Task  | Technology |
| -------- | ------- |
| Video Retrieval | YouTube Data API, google-api-python-client   |
| Transcription | yt-dlp, OpenAI Whisper     |
| User Interface  | Gradio   |

---
## Contributors
	•	Asif Khan – Developer and Project Lead
    •	Kade Thomas – Summarization Specialist
    •	Amit Gaikwad - Vector Database Specialist
    •	Simranpreet Saini – AI Agent Specialist
    •	Jason Brooks – Documentation Specialist
    
