# VidInsight AI: AI-Powered YouTube Content Analyzer

## Overview
VidInsight AI is an AI-powered application designed to analyze YouTube videos for a given subject, extract insights, provide transcriptions, topic, summary, key-points and a new content idea!\
The application is built to assist:
- content creators,
- educators & researchers, and
- everyday users in understanding video content quickly and effectively.

---
This ReadMe file documents the current phase of the project and will be updated as new features are implemented.

**Current Features:**

    1️⃣ Gradio User Interface

    ✔ Input:
    	•	Users enter a topic in a Gradio app to initiate the analysis.
    	•	The system processes the input and retrieves relevant videos.
    
    ✔ Output:
    	•	Displays video details (title, channel, views, publication date, etc.).
    	•	Provides a summary & key points of the selected videos.
    	•	Generates a brand-new content idea based on AI-driven insights.


    2️⃣ Configurable Filtering System

    ✔ A config file (config.py) allows fine-tuning of video selection:
    	•	Filters based on trusted channels, video duration, view counts, and teaching-related keywords.
    	•	Prioritizes high-quality educational content over noisy or irrelevant videos.
    	•	Ensures the retrieved videos are relevant to the selected topic.

    3️⃣ YouTube Video Retrieval

    ✔ Fetches up to 10 YouTube videos related to the user’s topic.
    ✔ Filters videos based on:
    	•	Keywords (e.g., tutorial, lesson, introduction, course).
    	•	View counts (ensures a minimum number of views for relevance).
    	•	Trusted channels (e.g., Khan Academy, DeepMind, OpenAI, Stanford).
    ✔ Selects the top 3 most relevant videos for further processing.    

    4️⃣ AI-Powered Transcription (Whisper Model)

    ✔ Downloads and extracts audio from the selected YouTube videos using yt-dlp.
    ✔ Transcribes the videos using OpenAI’s Whisper model.
    ✔ Saves complete transcriptions in the output/ folder for further processing.

    5️⃣ Vectorization & Storage in a Vector Database

    ✔ Embeds transcriptions using Hugging Face sentence-transformers.
    ✔ Stores embeddings in a Vector Database - Pinecone (others can be used e.g. Weaviate, or NeonDB).
    ✔ Enables efficient querying of video content for rapid analysis and comparisons.

    6️⃣ AI-Driven Summarization & Key Insights Extraction

    ✔ Retrieves stored transcriptions for multi-video summarization.
    ✔ AI-powered NLP analysis extracts:
    	•	Key discussion points from each video.
    	•	Common themes & unique insights from multiple videos.
    	•	Concise summaries for quick understanding.

    7️⃣ AI Content Ideation & Generation

    ✔ Uses Gemini AI + TAVILY API to generate a brand-new content idea based on extracted insights.
    ✔ Provides a detailed content creation plan, including:
    	•	Topic & Hook (engaging introduction).
    	•	Structured Outline (flow of discussion).
    	•	Key Discussion Points (what to cover).
    	•	Timeframe & Duration (how long it should be).
    	•	SEO-Optimized Metadata (tags, descriptions, and keywords).

    8️⃣ Actionable Output in the Gradio App

    ✔ Users receive structured insights in an easy-to-read format, including:
    	•	Summaries & key takeaways from multiple videos.
    	•	AI-generated content ideas tailored for content creators.
    	•	SEO-enhanced suggestions for video optimization.
    ✔ Speeds up research and content creation by eliminating manual analysis.
        
---

## Project Structure

VidInsight-AI/\
├── app.py                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Gradio web interface for user interaction\
├── config.py                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Configuration file for API keys and filters\
├── fetch_youtube_videos.py   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Fetches and filters YouTube videos\
├── transcribe_videos.py      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Transcribes videos and saves transcripts\
├── summary.py                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Generates summaries from transcriptions\
├── YouTubeAgent.py           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Creates content ideas using Gemini AI\
├── main.py                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # CLI-based alternative to run the app\
├── requirements.txt          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Project dependencies\
├── dbcone.py                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # storing embeddings in vector database\
├── embeddings.py             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # vectorizing corpus using sentence transformer\
├── keys1.env                 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Environment variables (API keys)\
└── output/                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Folder for saved transcripts\
&nbsp;&nbsp;&nbsp; └── <video_id>.txt     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Transcripts saved as text files\

### Key Components:
	1.	Interface Files:
    	•	`app.py`: Web interface using Gradio
    	•	`main.py`: Command-line interface
	2.	Core Processing Files:
    	•	`fetch_youtube_videos.py`: Video retrieval
    	•	`transcribe_videos.py`: Audio transcription
    	•	`summary.py`: Content summarization
    	•	`YouTubeAgent.py`: Content idea generation
        •	`dbcone.py`: storing embeddings in vector database
        •	`embeddings.py`: vectorizing corpus using sentence transformer
	3.	Configuration Files:
    	•	`config.py`: Settings and filters
    	•	`keys1.env`: API keys
    	•	`requirements.txt`: Dependencies
	4.	Output Directory:
    	•	`output/`: Stores generated transcripts

---

## Setup Instructions (need to be completed)

1. Prerequisites\
	•	Python 3.8 or higher\
	•	FFmpeg installed on the system (for audio processing)\
	•	A YouTube Data API key (create one via Google Cloud Console)\
	•	A GEMINI API key \
	•	A TAVILY API key 

3. Installation
	1.	Clone the repository:
      ```python
      git clone <repository_url>
      ```
   	2.	Install required dependencies:

   	3.	Set up your API key:
	•	Create a `.env` file or update `keys1.env` with your YouTube API key:
    ```python
    YOUTUBE_API_KEY="your_api_key_here"
    GEMINI_API_KEY="your_api_key_here"
    TAVILY_API_KEY="your_api_key_here"
    ```
   \
    
4. Running the Application\
	•	Using the Gradio Interface:
    ```python
    python app.py
    ```
    \
   •	Using the CLI:
    ```python
    python main.py
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
    	•	Topic, Summary, and Key-Points
    	•	A New Content Idea with Compreehensive Details    
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

## 🛠️ Technology Stack

| Task  | Technology |
| -------- | ------- |
| Video Retrieval | YouTube Data API, google-api-python-client   |
| Transcription | yt-dlp, OpenAI Whisper     |
| Summarization  | Gemini AI, LangChain  |
| Content Generation | Gemini AI, LangChain   |
| Vectorizaton | SentenceTransformer('all-MiniLM-L6-v2')   |
| Vector Database | Pinecone  |

---

## Known Issues
	1.	If no results are found or an error occurs during video fetching, the app displays an error message in JSON format.
	2.	Ensure that valid topics are entered; overly broad or unrelated topics may not yield meaningful results.

---

## Future Features        
	1.	Multilingual Support:
    	•	Add support for transcription in other languages (e.g., Spanish, French).
        
	2.	Interactive Q&A:
    	•	Allow users to ask questions about analyzed video content.

    3.	Platform Specific Content Creation:
        •	Allow users to specify platforms like Twitter, Youtube, Instagram etc. 

    4.	Teaching Course Creation:
        •	Educators can create teaching courses based on filtering appropriate contents

    2.	Scientific Integration:
        •	We can integrate API for research papers to get richer context for future steps

---

## 📌 Contributors
	•	Asif Khan – Project Lead, Developer & UI Specialist
    •	Kade Thomas – Summarization Specialist
    •	Amit Gaikwad - Vector Database Specialist
    •	Simranpreet Saini – AI Agent Specialist
    •	Jason Brooks – Documentation Specialist

---
## 🙏 Acknowledgements 
- Special thanks to Firas Obeid for being an advisor on the project
- Special thanks to OpenAI, Hugging Face, and YouTube API, Gemini API, and Tavily API for providing the tools that made this project possible. 🚀
