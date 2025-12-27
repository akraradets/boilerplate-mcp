from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP(
    name="Boilerplate-MCP",
    version="v0.0.1",
    # include_tags={},              # Only expose these tagged components
    # exclude_tags={},     # Hide these tagged components
    # on_duplicate_tools="error",                  # Handle duplicate registrations
    # on_duplicate_resources="warn",
    # on_duplicate_prompts="replace",    
    )

# Configure CORS for browser-based clients
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]

# This is how you can break MCP server into modular design
from server.calculator import mcp as calculator_mcp
mcp.mount(calculator_mcp, prefix="calculator")
from server.demo.context import mcp as demo_context
mcp.mount(demo_context, prefix="demo")

app = mcp.http_app(middleware=middleware)