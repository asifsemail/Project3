"""
# YouTube Video Fetcher Module

This module is responsible for searching, filtering, and retrieving educational YouTube videos based on user queries.

## Summary
- Fetches videos using YouTube Data API v3
- Filters videos based on:
  - Duration (medium length: 4-20 minutes)
  - View count (minimum threshold)
  - Teaching vs non-teaching keywords
  - Trusted educational channels
- Returns top 3 most relevant videos sorted by view count

## Dependencies

### System Requirements
- Python 3.8+
- Internet connection for API calls

### Package Dependencies
- google-api-python-client==2.104.0
  Install: `pip install google-api-python-client`

### Project Dependencies
1. config.py
   - Provides YOUTUBE_API_KEY
   - Contains FILTER_CONFIG dictionary with:
     - videoDuration
     - order
     - trusted_channels
     - teaching_keywords
     - non_teaching_keywords
     - max_results
     - min_view_count

2. Environment Setup
   - keys1.env file with YouTube API key
   - YouTube Data API access enabled in Google Cloud Console

## Returns
- List of dictionaries containing:
  - title: Video title
  - url: YouTube video URL
  - channel: Channel name
  - views: View count
- Or error message string if fetch fails

## Error Handling
- Returns error message if:
  - API key is invalid
  - API quota is exceeded
  - Network connection fails
  - YouTube API request fails
"""

# Import Dependencies
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, FILTER_CONFIG

def fetch_videos(topic):
    """Fetch relevant YouTube videos based on topic and filter criteria."""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Fetch videos from YouTube API
        search_response = youtube.search().list(
            q=topic,
            part="snippet",
            type="video",
            maxResults=FILTER_CONFIG["max_results"],  # Limit to max_results directly
            videoDuration=FILTER_CONFIG["videoDuration"],
            order=FILTER_CONFIG["order"]
        ).execute()

        # Process video results
        videos = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title'].lower()
            description = item['snippet']['description'].lower()
            channel_id = item['snippet']['channelId']
            
            # Fetch video statistics (views)
            stats_response = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()
            
            stats = stats_response.get('items', [{}])[0].get('statistics', {})
            view_count = int(stats.get("viewCount", 0))
            
            # Apply filters: minimum views, keywords, trusted channels
            if view_count < FILTER_CONFIG["min_view_count"]:
                continue
            
            teaching_score = len(set(title.split() + description.split()) & FILTER_CONFIG["teaching_keywords"])
            noise_score = len(set(title.split() + description.split()) & FILTER_CONFIG["non_teaching_keywords"])
            # noise_score = len(set(title.split() + description.split()) & FILTER_CONFIG["blocked_keywords"])
            
            is_trusted_channel = channel_id in FILTER_CONFIG["trusted_channels"].values()
            
            if teaching_score > noise_score or is_trusted_channel:
                videos.append({
                    'title': item['snippet']['title'],
                    'url': f'https://youtu.be/{video_id}',
                    'channel': item['snippet']['channelTitle'],
                    'views': view_count,
                })

        # Sort by views (descending) and return top 3 videos
        return sorted(videos, key=lambda x: x['views'], reverse=True)[:3]

    except Exception as e:
        return f"Error fetching videos: {str(e)}"
