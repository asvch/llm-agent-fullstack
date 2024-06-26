from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import json
from urllib import request
from langchain_community.tools import YouTubeSearchTool
from langchain_experimental.text_splitter import SemanticChunker
from bs4 import BeautifulSoup
import re
from langchain_elasticsearch import ElasticsearchStore
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import LLMMathChain

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Get API Keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
weather_api_key = os.getenv("weather_api_key")
ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")


BASE_WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


# Extract all dialogue of Romeo from Romeo & Juliet
soup = BeautifulSoup(open("Romeo.html", encoding="utf8"), "lxml")

dialogues = soup.find_all("p", class_="normalsans")

# Path to the output text file
output_file_path = "romeo_dialogues.txt"

# Write the dialogues to the text file
with open(output_file_path, "w") as file:

    for i in range(2, len(dialogues)):
        # remove brackets from lines and then save
        line = re.sub(r'\[.*?\]', '', dialogues[i].text)

        file.write("\n" + line)

embeddings = OpenAIEmbeddings()

text_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")

with open("romeo_dialogues.txt") as f:
  romeo_lines = f.read()

docs = text_splitter.create_documents([romeo_lines])

# Elasticsearch database
vectorstore = ElasticsearchStore.from_documents(
    docs,
    embeddings,
    index_name="openai-langchain-romeo-juliet4",   # Change index name whenever we change embedding method or there's an error
    es_cloud_id=ELASTIC_CLOUD_ID,
    es_api_key=ELASTIC_API_KEY,
)

llm = ChatOpenAI()

retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

# Create tools for LLM
# retriever for LLM Agent to answer questions about Romeo
retriever_tool = create_retriever_tool(
    retriever, "romeo_lines",          # give it info of the tool in plain English as well
    "Search for information about Romeo. For any questions about Romeo, you must use this tool!"
)

# web search tool for events LLM Agent was not trained on 
search_tavily = TavilySearchResults()
search_tool = Tool.from_function(
    name = "Tavily",
    func=search_tavily,
    description="Useful for browsing information from the Internet about current events, or information you are unsure of."
)

# weather tool
def build_weather_query(city_input):
    """
    Get the current weather in a given city.
    """

    url = (
        f"{BASE_WEATHER_API_URL}?key={weather_api_key}"
        f"&q={city_input}&aqi=yes"
    )

    response = request.urlopen(url)
    data = response.read()
    result = json.loads(data)

    # Return the temperature as a string
    return str(result["current"]["temp_f"])

weather_tool = Tool(
    name="Weather",
    func=build_weather_query,
    return_direct=False,  # Return the response directly to the LLM
    description="Use when you need to find the current weather in a given city."
)

# Math tool
problem_chain = LLMMathChain.from_llm(llm=llm)  # pass in our llm (ChatOpenAI llm we set earlier)
math_tool = Tool.from_function(name="Calculator",   # func comes from LLMMathChain library
                func = problem_chain.run,       # input plain English guidance about tool again
                 description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions."
                 )

# YouTube tool
youtube_search = YouTubeSearchTool()
yt_tool = Tool.from_function(
    name="YouTube",
    func=youtube_search.run,
    description="Use when you need to find a youtube video."
)

message_history = ChatMessageHistory()

tools = [retriever_tool, math_tool, search_tool, weather_tool, yt_tool]

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages(
    [                                      # System prompt in plain English
        ("system", "You are Romeo from Romeo and Juliet. You must answer any and all questions in first person using Romeo's speech style and in Early Modern English."),
        MessagesPlaceholder("chat_history", optional=True),  # pass in chat history
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),  # format required for Agent by LangChain
    ]
)

agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)