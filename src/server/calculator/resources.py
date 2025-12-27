from fastmcp import FastMCP
from fastmcp.resources import FileResource
from fastmcp.exceptions import ResourceError
import aiofiles # type: ignore
from pathlib import Path

mcp = FastMCP(
    name="Calculcator-resources",
    version="v0.0.1",
    )

data_path:Path = Path("data/")
story_path:Path = data_path.joinpath("stories")

# This is lazy load, it won't break if the file is missing
# Only when the resource is called, then it breaks
@mcp.resource("files://story1")
async def read_story1() -> str:
    """Load the story1 from the file"""
    file = story_path.joinpath("story1.txt")
    try:
        async with aiofiles.open(file, mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        raise ResourceError(f"File={file.resolve()} not found")
    

# This check the file existance first.
story2_path:Path = story_path.joinpath("story2.txt")
if story2_path.exists():
    # Use a file:// URI scheme
    readme_resource = FileResource(
        uri="files://story2", # type: ignore
        path=story2_path.resolve(), # Path to the actual file
        name="read_story2",
        description="Load the story2 from the file",
        mime_type="text/plain"
    )
    mcp.add_resource(readme_resource)

# Here, let's the client pick the filename
@mcp.resource("files://{story_name}")
async def read_stories(story_name:str) -> str:
    """Load the story from the `story_name`"""
    file = story_path.joinpath(f"{story_name}.txt")
    try:
        async with aiofiles.open(file, mode="r") as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        raise ResourceError(f"File={file.resolve()} not found")