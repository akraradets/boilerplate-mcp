from fastmcp import FastMCP
from server.calculator.tools import mcp as tools
from server.calculator.resources import mcp as resources
from server.calculator.prompts import mcp as prompts

mcp = FastMCP(
    name="Calculcator",
    version="v0.0.1",
    )

mcp.mount(server=tools)
mcp.mount(server=resources)
mcp.mount(server=prompts)