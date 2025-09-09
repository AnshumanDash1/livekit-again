import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from browser_use import Agent, ChatGoogle, Browser
from dotenv import load_dotenv
import asyncio


@function_tool()
async def get_weather(
        context: RunContext,  # type: ignore
        city: str) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


@function_tool()
async def search_web(
        context: RunContext,  # type: ignore
        query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."

@function_tool()
async def browser_use(
        context: RunContext,  # type: ignore
        query: str):
    """
    Directly control the user's browser to do tasks.
    """
    llm = ChatGoogle(model="gemini-2.5-flash")
    task = query
    browser = Browser(
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        user_data_dir='~/Library/Application Support/Google/Chrome',
        profile_directory='Default',
    )
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser
    )
    asyncio.create_task(agent.run())