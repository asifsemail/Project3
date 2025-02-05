"""
# Configuration Module for VidInsight AI

This module manages configuration settings and environment variables for the VidInsight AI project.

## Summary
- Loads API keys from environment file
- Defines filtering criteria for YouTube video search
- Configures trusted educational channels
- Sets up keyword-based content filtering
- Establishes quality thresholds (views, duration)

## Dependencies

### System Requirements
- Python 3.8+
- Read access to environment file location

### Package Dependencies
1. **python-dotenv**
   - Install: `pip install python-dotenv`
   - Purpose: Load environment variables from file

### Project Dependencies
1. **keys1.env file**
   - Must contain:
     - YOUTUBE_API_KEY
   - Format:
     ```
     YOUTUBE_API_KEY=your_youtube_api_key_here
     ```
   - Location: Project root directory

## Configuration Parameters

### Video Search Settings
- videoDuration: "medium" (4-20 minutes)
- order: "relevance"
- max_results: 10 videos per search
- min_view_count: 10,000 views threshold

### Content Filtering
1. Trusted Channels (Whitelist):
   - Khan Academy
   - edX
   - Coursera

2. Keyword Filters:
   - Teaching Keywords (Positive):
     {tutorial, lesson, course, how-to, introduction, basics}
   - Non-Teaching Keywords (Negative):
     {fun, experiment, joke, prank, vlog}

## Notes
- Keep keys1.env secure and never commit to version control
- Adjust filter criteria as needed for different use cases
- Channel IDs must be exact matches for trusted channel filtering

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
    # "blocked_keywords": {"fun", "experiment", "joke", "prank", "vlog"},
    "max_results": 10,          # Limit search results to 10 videos
    "min_view_count": 10000     # Minimum view count for relevance
}