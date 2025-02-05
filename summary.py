"""
# Video Summary Generator Module

This module processes transcribed video content to generate summaries, key points, and topic titles 
using Google's Gemini AI model.

## Summary
- Takes multiple video transcriptions as input
- Concatenates transcriptions for unified analysis
- Uses Gemini AI to generate:
  - Relevant topic title
  - Concise content summary
  - Key points from the content
- Handles response parsing and error cases

## Dependencies

### System Requirements
- Python 3.8+
- Internet connection for API calls

### Package Dependencies
1. **langchain-google-genai**
   - Install: `pip install langchain-google-genai`
   - Purpose: Interface with Gemini AI model

2. **python-dotenv**
   - Install: `pip install python-dotenv`
   - Purpose: Load environment variables

### Project Dependencies
1. **keys1.env file**
   - Must contain: GEMINI_API_KEY
   - Format: GEMINI_API_KEY=your_api_key_here

2. **Input Requirements**
   - Transcription texts from processed videos
   - Non-empty transcription content

## Functions
generate_combined_summary_and_key_points(transcriptions)
- Args: List of transcription texts
- Returns: Tuple of (topic_title, summary, key_points)
- Error Returns: Error messages with empty lists if processing fails

## Returns
Tuple containing:
1. topic_title (str): Generated title for the content
2. summary (str): Concise summary of all transcriptions
3. key_points (list): List of main points extracted

## Error Handling
- Returns error messages if:
  - Transcriptions are empty
  - Gemini API fails to respond
  - Response parsing fails
"""

import os
import glob
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def generate_combined_summary_and_key_points(transcriptions):
    if not all(transcriptions):
        return "Error: No transcription text provided.", [], ""

    # Concatenate the transcriptions into one single string
    concatenated_transcriptions = "\n".join(transcriptions)

    prompt = f"""
    The following are transcriptions of videos:
    ---
    {concatenated_transcriptions}
    ---
    Based on the content, generate a relevant topic title for the transcriptions. 
    Then, summarize the key insights and extract the main points from these transcriptions together. 
    Ignore sponsors and focus more on the details rather than the overall outline.
    Format your response as:
    Topic Title: [Generated topic title]
    
    Summary:
    [Concise summary of the transcriptions]
    
    Key Points:
    - [Key point 1]
    - [Key point 2]
    - [Key point 3]
    """
    # Load environment variables
    load_dotenv(find_dotenv('keys1.env'))

    # Get API key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-1.5-flash"

    # Initialize Gemini API
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, api_key=GEMINI_API_KEY)

    # Generate the response from the model
    response = llm.predict(prompt)
    
    if not response:
        return "Error: No response generated.", [], ""

    # Extract topic title, summary, and key points from response
    topic_title_start = response.find("Topic Title:")
    summary_start = response.find("Summary:")
    key_points_start = response.find("Key Points:")

    if topic_title_start != -1 and summary_start != -1 and key_points_start != -1:
        topic_title = response[topic_title_start + len("Topic Title:"): summary_start].strip()
        summary = response[summary_start + len("Summary:"): key_points_start].strip()
        key_points_str = response[key_points_start + len("Key Points:"):].strip()
        key_points = [point.strip(" -") for point in key_points_str.split("\n")]
    else:
        topic_title = "Error: Unable to generate topic title."
        summary = "Error: Unable to extract summary."
        key_points = []

    return topic_title, summary, key_points

