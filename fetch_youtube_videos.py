"""
# YouTube Video Fetcher for VidInsight AI

This module fetches and filters YouTube videos based on a user-provided topic. 
It uses the YouTube Data API to search for videos, applies filtering criteria, 
and returns the top 3 most relevant videos.

## Dependencies
1. **google-api-python-client**: For interacting with the YouTube Data API.
   - Install via: `pip install google-api-python-client`
2. **config.py**: Contains the `YOUTUBE_API_KEY` and `FILTER_CONFIG` dictionary.
   - Ensure the `.env` file is configured with your YouTube API key.

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
