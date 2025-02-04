import gradio as gr
from fetch_youtube_videos import fetch_videos
from transcribe_videos import transcribe_and_save
from embeddings import mainApp

def analyze(topic):
    """
    Fetch videos, transcribe them, and save transcripts.
    Args:
        topic (str): The topic to search for on YouTube.
    Returns:
        list: Contains video details and transcription paths.
    """
    try:
        # Fetch videos based on topic
        videos = fetch_videos(topic)
        
        if isinstance(videos, str):  # If an error message is returned
            return {"error": videos}
        
        if not videos:  # No videos found
            return {"error": "No relevant videos found for this topic."}
        
        results = []
        for video in videos:
            transcription_result = transcribe_and_save(video['url'])
            
            if "error" in transcription_result:
                results.append({
                    'Video': video['title'],
                    'Channel': video['channel'],
                    'Views': video['views'],
                    'Transcript Preview': transcription_result["error"]
                })
            else:
                results.append({
                    'Video': video['title'],
                    'Channel': video['channel'],
                    'Views': video['views'],
                    'Transcript Preview': transcription_result["transcription"][:500] + "...",
                    'Transcript File': transcription_result["file_path"]
                })
                
        mainApp()
        
        return results

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Create Gradio interface
gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(label="Enter learning topic"),
    outputs=gr.JSON(label="Results"),
    title="VidInsight Basic",
    description="Enter any topic to get educational video transcripts"
).launch()

