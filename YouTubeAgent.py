"""
# YouTube Content Idea Generator Module

This module leverages Google's Gemini AI to generate structured content ideas for YouTube videos
based on provided summaries and key points.

## Summary
- Uses Gemini AI model for content generation
- Creates detailed video proposals including:
  - Title and hook
  - Main talking points
  - Video structure
  - Thumbnail concepts
  - Target audience
  - SEO keywords
- Formats output with clear section separation

## Dependencies

### System Requirements
- Python 3.8+
- Internet connection for API calls

### Package Dependencies
1. **langchain-google-genai**
   - Install: `pip install langchain-google-genai`
   - Purpose: Interface with Gemini AI model

2. **langchain-community**
   - Install: `pip install langchain-community`
   - Purpose: Access to Tavily search tools

3. **python-dotenv**
   - Install: `pip install python-dotenv`
   - Purpose: Load environment variables

### Project Dependencies
1. **keys1.env file**
   - Must contain:
     - GEMINI_API_KEY
     - TAVILY_API_KEY
   - Format:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     TAVILY_API_KEY=your_tavily_api_key
     ```

2. **Input Requirements**
   - Dictionary containing:
     - summary: Text summarizing content
     - keypoints: List of key points

## Functions
generateidea(input)
- Args: Dictionary with 'summary' and 'keypoints'
- Returns: Formatted string containing structured content idea
- Error Returns: Error message if generation fails

## Returns
Structured string containing:
1. Title
2. Description/Hook
3. Main Talking Points
4. Video Structure
5. Thumbnail Concepts
6. Target Audience
7. Estimated Length
8. SEO Keywords

## Error Handling
- Returns error message if:
  - API keys are missing
  - API calls fail
  - Response formatting fails
"""


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv, find_dotenv
import os
from langchain.agents import initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools

# Load environment variables
load_dotenv(find_dotenv('keys1.env'))

# Set the model name and API keys
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def generateidea(input):
    """Generate content ideas based on summary and key points."""
    try:
        # Initialize the model with higher temperature for creativity
        llm = ChatGoogleGenerativeAI(
            google_api_key=GEMINI_API_KEY,
            model=GEMINI_MODEL,
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=2048  # Ensure longer output
        )
        
        # Create a specific prompt template
        prompt = f"""
        Based on this content:
        Summary: {input["summary"]}
        Key Points: {input["keypoints"]}

        Generate a detailed YouTube video idea using exactly this format:

        1. **Title:**
        [Create an attention-grabbing, SEO-friendly title]

        2. **Description/Hook:**
        [Write 2-3 compelling sentences that hook viewers]

        3. **Main Talking Points:**
        • [Main point 1]
        • [Main point 2]
        • [Main point 3]
        • [Main point 4]
        • [Main point 5]

        4. **Suggested Video Structure:**
        • [00:00-02:00] Introduction
        • [02:00-05:00] First Topic
        • [05:00-08:00] Second Topic
        • [08:00-12:00] Third Topic
        • [12:00-15:00] Examples and Applications
        • [15:00-17:00] Conclusion

        5. **Potential Thumbnail Concepts:**
        • [Thumbnail idea 1]
        • [Thumbnail idea 2]
        • [Thumbnail idea 3]

        6. **Target Audience:**
        [Describe ideal viewer demographic and background]

        7. **Estimated Video Length:**
        [Specify length in minutes]

        8. **Keywords for SEO:**
        [List 8-10 relevant keywords separated by commas]

        Ensure each section is detailed and properly formatted.
        """

        # Generate response directly with LLM
        response = llm.predict(prompt)
        
        # Format the response
        formatted_response = response.replace("1. **", "\n\n1. **")
        formatted_response = formatted_response.replace("2. **", "\n\n2. **")
        formatted_response = formatted_response.replace("3. **", "\n\n3. **")
        formatted_response = formatted_response.replace("4. **", "\n\n4. **")
        formatted_response = formatted_response.replace("5. **", "\n\n5. **")
        formatted_response = formatted_response.replace("6. **", "\n\n6. **")
        formatted_response = formatted_response.replace("7. **", "\n\n7. **")
        formatted_response = formatted_response.replace("8. **", "\n\n8. **")
        
        return formatted_response.strip()

    except Exception as e:
        return f"Error generating content idea: {str(e)}"


