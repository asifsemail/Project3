"""
# Configuration File for VidInsight AI

This file contains the configuration settings for the VidInsight AI project, including:
- API keys
- Filtering criteria for YouTube video retrieval
- Trusted channels and keyword-based filtering

## Notes:
- Ensure the `.env` file is properly set up with the required API key.
- Adjust the filtering criteria based on project requirements.
"""


# dependencies
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env file
load_dotenv(find_dotenv('keys1.env'))

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Content Filter Settings
FILTER_CONFIG = {
    "videoDuration": "medium",  # Focus on videos between 4 and 20 minutes
    "order": "relevance",       # Sort by relevance
    # Trusted Channels: Only videos from these channels will bypass keyword filters
    "trusted_channels": {
        "Khan Academy": "UC4a-Gbdw7vOaccHmFo40b9g",
        "edX": "UCEBb1b_L6zDS3xTUrIALZOw",
        "Coursera": "UC58aowNEXHHnflR_5YTtP4g",
    },
    "teaching_keywords": {"tutorial", "lesson", "course", "how-to", "introduction", "basics"}, # Videos containing these words are prioritized
    "non_teaching_keywords": {"fun", "experiment", "joke", "prank", "vlog"}, #Videos containing these words are deprioritized or ignored
    "max_results": 10,          # Limit search results to 10 videos
    "min_view_count": 10000     # Minimum view count for relevance
}