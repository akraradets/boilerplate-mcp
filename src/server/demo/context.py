# This is for demoing the context
# https://gofastmcp.com/servers/context
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.server.context import Context
import asyncio

from dataclasses import dataclass

mcp = FastMCP(
    name="ContextDemo",
    version="v0.0.1",
    )

@dataclass
class UserInfo:
    name: str
    age: int

@dataclass
class ElicitResult:
    action: str
    data: UserInfo

@mcp.tool
async def process_file(file_uri: str, ctx: Context = CurrentContext()) -> str:
    """Processes a file, using context for logging and resource access."""

    # Do some logging
    # The client will receive a notification from while waiting for the processing
    await ctx.report_progress(progress=0, total=100) 
    await ctx.debug("Starting analysis")
    await asyncio.sleep(1)
    await ctx.report_progress(progress=20, total=100) 
    await ctx.info(f"Processing {len(file_uri)} items") 
    await asyncio.sleep(2)
    await ctx.report_progress(progress=50, total=100) 
    await ctx.warning("Deprecated parameter used")
    await ctx.report_progress(progress=100, total=100) 
    result_elicit:ElicitResult = await ctx.elicit(
        message="Give me this new parameter",
        response_type=UserInfo  # type: ignore
    )
    if result_elicit.action == "accept":
        user:UserInfo = result_elicit.data
        await asyncio.sleep(1)
        return f"Hello {user.name}, you are {user.age} years old"
    elif result_elicit.action == "decline":
        sample_result = await ctx.sample(f"Please provide the reason of declined")
        await ctx.info(f"Operation cancelled with:{sample_result}")
        return "Information not provided"
    else:  # cancel
        await ctx.error("Operation cancelled")
        return "Operation cancelled"
    

# https://gofastmcp.com/servers/sampling#defining-tools
# https://gofastmcp.com/servers/sampling#loop-control
# This won't work in `MCP Inspector`
# I put it here because it looks kind of cool. But how to use this. IDK

from mcp.types import SamplingMessage

def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

def get_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

@mcp.tool
async def controlled_agent(question: str, ctx: Context) -> str:
    """Agent with manual loop control."""
    messages: list[str | SamplingMessage] = [question]  # strings auto-convert

    while True:
        step = await ctx.sample_step(
            messages=messages,
            tools=[search, get_time],
        )

        if step.is_tool_use:
            # Tools already executed (execute_tools=True by default)
            # Log what was called before continuing
            for call in step.tool_calls:
                print(f"Called tool: {call.name}")

        if not step.is_tool_use:
            return step.text or ""

        # Continue with updated history
        messages = step.history