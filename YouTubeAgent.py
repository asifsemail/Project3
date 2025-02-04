from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv, find_dotenv
import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate

 # Additional imports for agent with built-in tools.
from langchain.agents import initialize_agent, load_tools
from langchain.schema import HumanMessage, SystemMessage

 # Load environment variables.
load_dotenv(find_dotenv("keys.env"))

# Set the model name for our LLMs.
GEMINI_MODEL = "gemini-1.5-flash"
# Store the API key in a variable.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def generateidea(input):
 # Initialize the model.
    llm = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY, model=GEMINI_MODEL, temperature=0.3)


    # Set up the built-in wikipedia tool.
    tools = [TavilySearchResults(max_results=1)]

    # Initialize the agent.
    agent = initialize_agent(tools, agent="chat-zero-shot-react-description", verbose=True, llm=llm)

    # Create a list containing a system message and a human message.
    query = {
        "input":
                    f"""
                    You are a youtuber trying to generate a novel and original YouTube video idea based on a summary and key points. Your job is to provide the following:
                    1. An attention-grabbing title
                    2. A brief description/hook
                    3. Main talking points
                    4. Suggested video structure
                    5. Potential thumbnail concepts
                    6. Target audience
                    7. Estimated video length
                    8. Keywords for SEO

                    Do not use "see above" in the final answer.

                    Summary: {input["summary"]}
                    Key Points: {input["keypoints"]}
                    """
    }

    result = agent.run(query)
    print(result)