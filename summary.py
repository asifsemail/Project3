import os
import glob
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv(find_dotenv('keys1.env'))

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

# Initialize Gemini API
llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, api_key=GEMINI_API_KEY)

# Define the directory path for text files
output_dir = os.path.join(os.path.dirname(__file__), "Output")

# Get a list of all .txt files in the directory
txt_files = glob.glob(os.path.join(output_dir, "*.txt"))

# Ensure there are files to process
if not txt_files:
    print("No .txt files found in Output directory.")
    exit()

# Dictionary to store file contents
file_contents = {}

# Read and store contents
for file_path in txt_files:
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents[os.path.basename(file_path)] = file.read()


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
        key_points = [point.strip(" -") for point in key_points_str.split("\n") if point]
    else:
        topic_title = "Error: Unable to generate topic title."
        summary = "Error: Unable to extract summary."
        key_points = []

    return topic_title, summary, key_points

# Combine all transcriptions into one list
transcriptions = list(file_contents.values())

# Get topic title, combined summary, and key points from Gemini
topic_title, combined_summary, combined_key_points = generate_combined_summary_and_key_points(transcriptions)

# Print topic title, combined summary, and key points
print("Topic Title:", topic_title)
print('--------------------------------------------')
print("Combined Summary:", combined_summary)
print('--------------------------------------------')
print("Combined Key Points:", combined_key_points)

