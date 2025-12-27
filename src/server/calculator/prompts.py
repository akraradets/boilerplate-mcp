from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptResult 
from fastmcp.prompts.prompt import PromptMessage, TextContent # type: ignore

mcp = FastMCP(
    name="Calculcator-prompts",
    version="v0.0.1",
    )

# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
    """Generates a user message asking for an explanation of a topic."""
    return f"Can you please explain the concept of '{topic}'?"

# Prompt returning a specific message type
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """Generates a user message requesting code generation."""
    content = f"Write a {language} function that performs the following task: {task_description}"
    return PromptMessage(role="user", content=TextContent(type="text", text=content))

# Prompt returning a list of PromptMessage
@mcp.prompt
def roleplay_scenario(character: str, situation: str) -> PromptResult:
    """Sets up a roleplaying scenario with initial messages."""
    return [
        Message(f"Let's roleplay. You are {character}. The situation is: {situation}"),
        Message("Okay, I understand. I am ready. What happens next?", role="assistant")
    ]