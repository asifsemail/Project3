"""
# Main Application Module (Gradio Interface)

This module provides the web interface and core functionality for the VidInsight AI application,
integrating video fetching, transcription, summarization, and content idea generation.

## Summary
- Creates a Gradio web interface
- Processes user topic input
- Coordinates video fetching and transcription
- Generates summaries and content ideas
- Displays results in a formatted JSON output

## Dependencies

### System Requirements
- Python 3.8+
- Internet connection for API calls
- FFmpeg for audio processing

### Package Dependencies
1. **gradio==3.50.2**
   - Install: `pip install gradio`
   - Purpose: Web interface creation

2. **Other Project Packages**
   - fetch_youtube_videos
   - transcribe_videos
   - summary
   - YouTubeAgent

### Project Dependencies
1. **Local Modules**
   - fetch_youtube_videos.py: For YouTube video retrieval
   - transcribe_videos.py: For video transcription
   - summary.py: For generating summaries
   - YouTubeAgent.py: For content idea generation

2. **Output Directory**
   - 'output/' folder for saving transcriptions

## Functions

1. format_results(results)
   - Formats view counts with commas
   - Cleans transcript preview text
   
2. analyze(topic)
   - Main processing function
   - Coordinates all operations:
     - Video fetching
     - Transcription
     - Summary generation
     - Content idea creation

## Returns
JSON output containing:
1. Video Information
   - Title
   - Channel
   - Views
   - Transcript preview
   - File paths
2. Analysis
   - Topic title
   - Summary
   - Key points
   - Content ideas

## Error Handling
- Empty topic validation
- Video fetching errors
- Transcription failures
- Analysis generation issues

"""


import gradio as gr
from fetch_youtube_videos import fetch_videos
from transcribe_videos import transcribe_and_save
from summary import generate_combined_summary_and_key_points
from YouTubeAgent import generateidea
from embeddings import mainApp

def format_results(results):
    """Format results for better display"""
    if isinstance(results, list):
        for result in results:
            if 'Views' in result:
                result['Views'] = f"{result['Views']:,}"  # Format numbers with commas
            if 'Transcript Preview' in result:
                result['Transcript Preview'] = result['Transcript Preview'].replace('\n', ' ')
    return results

def analyze(topic):
    """
    Fetch videos, transcribe them, and generate analysis including summaries and content ideas.
    """
    if not topic.strip():
        return {"error": "⚠️ Please enter a topic to analyze"}
    
    try:
        # Fetch videos based on topic
        videos = fetch_videos(topic)
        
        if isinstance(videos, str):
            return {"error": f"⚠️ {videos}"}
        
        if not videos:
            return {"error": "⚠️ No relevant videos found for this topic."}
        
        results = []
        transcriptions = []  # Store transcriptions for summary generation
        
        # Process each video
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
                # Add transcription for summary generation
                transcriptions.append(transcription_result["transcription"])
        
        # Generate summary and content ideas if transcriptions exist
        if transcriptions:
            
            mainApp(topic)
            
            topic_title, summary, key_points = generate_combined_summary_and_key_points(transcriptions)
            
            # Generate content idea
            input_for_idea = {
                "summary": summary,
                "keypoints": key_points
            }
            content_idea = generateidea(input_for_idea)
            
            # Add analysis to results
            results.append({
                "Analysis": {
                    "Topic Title": topic_title,
                    "Summary": summary,
                    "Key Points": key_points,
                    "Content Idea": content_idea
                }
            })
        
        return format_results(results)

    except Exception as e:
        return {"error": f"⚠️ An unexpected error occurred: {str(e)}"}

# Create Gradio interface with improved styling
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🎥 VidInsight AI
        ### AI-Powered YouTube Content Analyzer
        
        This tool helps you:
        - 📝 Get transcriptions of educational videos
        - 📊 Generate summaries and key points
        - 💡 Create content ideas
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label="Enter Topic",
                placeholder="e.g., Machine Learning, Data Science, Python Programming",
                lines=2
            )
            
        with gr.Column(scale=1):
            submit_btn = gr.Button("🔍 Analyze", variant="primary")
            clear_btn = gr.Button("🗑️ Clear")
    
    with gr.Row():
        output = gr.JSON(
            label="Analysis Results",
            show_label=True
        )
    
    # Add footer
    gr.Markdown(
        """
        ---
        📌 **Note**: This tool analyzes educational YouTube videos and generates AI-powered insights.
        
        Made by VidInsight Team 🤖
        """
    )
    
    # Set up button actions
    submit_btn.click(
        fn=analyze,
        inputs=topic_input,
        outputs=output,
        api_name="analyze"
    )
    clear_btn.click(lambda: None, None, topic_input, queue=False)

if __name__ == "__main__":
    app.launch()



