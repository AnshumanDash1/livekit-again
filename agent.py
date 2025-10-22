import os

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, openai
from livekit.plugins import google
from simple_prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
# from tools import get_weather, search_web, browser_use
from browser_nav_tools import navigate, click_text, type_into, get_accessibility_tree
from prompts.prompt_loader import get_prompt
# from mcp_client import MCPServerSse
# from mcp_client.agent_tools import MCPToolsIntegration

load_dotenv(".env")
# to start, do uv run agent.py console


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=get_prompt("vo_screen_reader"),
            tools = [navigate, click_text, type_into, get_accessibility_tree]
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral"
        )
    )
    # mcp_server = MCPServerSse(
    #     params={"url": os.environ.get("PLAYWRIGHT_MCP_URL")},
    #     cache_tools_list=True,
    #     name="SSE MCP Server"
    # )
    # agent = await MCPToolsIntegration.create_agent_with_tools(
    #     agent_class=Assistant,
    #     mcp_servers=[mcp_server]
    # )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))