from fetch_youtube_videos import fetch_videos
from transcribe_videos import transcribe
from embedding import mainApp

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
    mainApp()
