from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.agents import create_agent 
from langchain.agents.middleware import wrap_tool_call
from rich import print
from langchain_tavily import TavilySearch
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@tool
def get_weather(city: str) -> str:
    """Returns the weather information"""

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Weather API error: {data.get('message', 'Unknown error')}"

    data = response.json()
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    return f"weather of {city}: {desc}, {temp} degree C"


@tool
def get_news(city: str) -> str:
    """Get latest news about city"""
    query = f"latest news of {city}"
    tool = TavilySearch(
        max_results=3,
        topic="news"
    )

    city_news = tool.invoke({"query": query})
    news_items = city_news.get("results",[])

    if not news_items:
        return f"No news results found for {city}."
    
    news_list = []

    for news in news_items:
        news_list.append(f"'url':{news['url']},'title':{news['title']}, 'content':{news['content'][:150]}")

    return "\n".join(news_list)

@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call"""
    tool_name = request.tool_call['name']
    confirm = input(f"Agent wants to call '{tool_name}' tool. Approve?(yes/no): ")

    if confirm.lower() != "yes":
        return ToolMessage(
            content="calling tool is denied",
            tool_call_id = request.tool_call['id']
        )

    return handler(request)


llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

agent = create_agent(
    llm,
    tools=[get_news,get_weather],
    system_prompt=(
        "You are a helpful city assistant. "
        "Use the available tools when current weather "
        "or recent city news is requested. "
        "Explain the results clearly and concisely."
    ),
    middleware=[human_approval]
    )

print("CITY ASSISTANT | enter exit to quit")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    print("Bot:", result['messages'][-1].content[0]['text'])




