import asyncio
from fastmcp import Client
from mcp.types import SamplingCapability
from mcp.types import Tool, Resource, ResourceTemplate, Prompt
from fastmcp.client.elicitation import ElicitResult, ElicitRequestParams, RequestContext
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext

import logging
from fastmcp.client.logging import LogMessage

############# Handlers #################

# In a real app, you might configure this in your main entry point
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger for the module where the client is used
logger = logging.getLogger(__name__)

# This mapping is useful for converting MCP level strings to Python's levels
LOGGING_LEVEL_MAP = logging.getLevelNamesMapping()

async def log_handler(message: LogMessage):
    """
    Handles incoming logs from the MCP server and forwards them
    to the standard Python logging system.
    """
    msg = message.data.get('msg')
    extra = message.data.get('extra')

    # Convert the MCP log level to a Python log level
    level = LOGGING_LEVEL_MAP.get(message.level.upper(), logging.INFO)

    # Log the message using the standard logging library
    logger.log(level, msg, extra=extra)

async def elicitation_handler(message: str, response_type: type, params: ElicitRequestParams, context: RequestContext):
    print(f"Server asks: {message}")
    # crafting response
    response = {}
    for key, value in params.requestedSchema["properties"].items():
        key = key
        title = value["title"]
        field_type = value["type"]
        user_response = input(f"{title}:{field_type} - ")
        if(field_type == "int"):
            user_response = int(user_response)
        response[key] = user_response

    # Simple text input for demonstration
    
    if not response:
        # For non-acceptance, use ElicitResult explicitly
        return ElicitResult(action="decline")
    
    # Use the response_type dataclass to create a properly structured response
    # FastMCP handles the conversion from JSON schema to Python type
    # Return data directly - FastMCP will implicitly accept the elicitation
    return ElicitResult(action="accept", content=response)


async def progress_handler(
    progress: float, 
    total: float | None, 
    message: str | None
) -> None:
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {percentage:.1f}% - {message or ''}")
    else:
        print(f"Progress: {progress} - {message or ''}")



async def basic_sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    # Extract message content
    conversation = []
    for message in messages:
        content = message.content.text if hasattr(message.content, 'text') else str(message.content)
        conversation.append(f"{message.role}: {content}")
        print(message)
    # Use the system prompt if provided
    system_prompt = params.systemPrompt or "You are a helpful assistant."

    # Here you would integrate with your preferred LLM service
    # This is just a placeholder response
    return f"Response based on conversation: {' | '.join(conversation)}"


################ Client Logic ###################

# HTTP server
client = Client("http://localhost:8080/mcp",
                # sampling_capabilities=SamplingCapability(),
                sampling_handler=basic_sampling_handler,
                elicitation_handler=elicitation_handler,
                log_handler=log_handler,
                progress_handler=progress_handler)


def list_tools(tools:list[Tool]):
    print("========tool========")
    for tool in tools:
        print(f"Tool: {tool.name}")
        print(f"Description: {tool.description}")
        if tool.inputSchema:
            print(f"Parameters: {tool.inputSchema}")
        # Access tags and other metadata
        if hasattr(tool, 'meta') and tool.meta:
            fastmcp_meta = tool.meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
        print()
    print()

def list_resources(resources:list[Resource]):
    print("========resource========")
    for resource in resources:
        print(f"Resource URI: {resource.uri}")
        print(f"Name: {resource.name}")
        print(f"Description: {resource.description}")
        print(f"MIME Type: {resource.mimeType}")
        # Access tags and other metadata
        if hasattr(resource, '_meta') and resource._meta:
            fastmcp_meta = resource._meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
        print()
    print()

def list_resource_templates(templates:list[ResourceTemplate]):
    print("========template========")
    for template in templates:
        print(f"Template URI: {template.uriTemplate}")
        print(f"Name: {template.name}")
        print(f"Description: {template.description}")
        # Access tags and other metadata
        if hasattr(template, '_meta') and template._meta:
            fastmcp_meta = template._meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
        print()
    print()

def list_prompts(prompts:list[Prompt]):
    print("========prompt========")
    for prompt in prompts:
        print(f"Prompt: {prompt.name}")
        print(f"Description: {prompt.description}")
        if prompt.arguments:
            print(f"Arguments: {[arg.name for arg in prompt.arguments]}")
        # Access tags and other metadata
        if hasattr(prompt, '_meta') and prompt._meta:
            fastmcp_meta = prompt._meta.get('_fastmcp', {})
            print(f"Tags: {fastmcp_meta.get('tags', [])}")
        print()
    print()

def progress_handler(progress):
    print(progress)

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        coros = [
            asyncio.create_task(client.list_tools()),
            asyncio.create_task(client.list_resources()),
            asyncio.create_task(client.list_resource_templates()),
            asyncio.create_task(client.list_prompts())
        ]
        results = await asyncio.gather(*coros)        
        print(results)
        # List available operations
        list_tools(results[0])
        list_resources(results[1])
        list_resource_templates(results[2])
        list_prompts(results[3])
        
        # Execute operations
        # This tool also use Elicitation
        # result = await client.call_tool(
        #     "demo_process_file", 
        #     arguments={"file_uri":"this_file.txt"})
        # print(result)

        result = await client.call_tool(
            "demo_controlled_agent",
            arguments={"question":"Why do I do this?"}
        )
        print(result)


asyncio.run(main())