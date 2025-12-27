# Boilerplate MCP

This repository follow the tutorial [here](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#server)

- [Boilerplate MCP](#boilerplate-mcp)
  - [From Zero to Hero](#from-zero-to-hero)
  - [This repository](#this-repository)
  - [Developing tools](#developing-tools)
    - [FastMCP](#fastmcp)
    - [MCP Inspector](#mcp-inspector)
  - [MCP Server](#mcp-server)
    - [Stateful VS Stateless](#stateful-vs-stateless)
    - [Transport option](#transport-option)
    - [Running the server](#running-the-server)
  - [MCP Client](#mcp-client)
    - [Running the Client](#running-the-client)


## From Zero to Hero

There are many resources out there teaching you about MCP.
What I have found is it usually an overview, thus too simple.

Anyhow, they are great when you start to learn this new thing.

Hence,  I recommend you this series of youtue videos for you to watch.

1. MCP In 26 Minutes (Model Context Protocol): https://www.youtube.com/watch?v=kOhLoixrJXo
2. you need to learn MCP RIGHT NOW!! (Model Context Protocol): https://www.youtube.com/watch?v=GuTcle5edjk

They talk about MCP from overview/general use to developing (sort of vibe coding level).

Now, when it comes to an actual developing a MCP server, you will need to do the document reading yourself.
The only good place to do that is here: https://modelcontextprotocol.io

## This repository

This repository is the boilerplate/template for developing a MCP server.
It provides

1. Resources/steps for learning MCP
2. A devcontainer/environment setup for MCP server development

## Developing tools

### FastMCP

[link](https://gofastmcp.com/getting-started/welcome)

`MCP` is a protocol. 
`FastMCP` is a framework that helps you build MCP servers quickly which seem to be something else than the `MCP SDK` and build on top of the idea of `FastAPI`.

If you know `FastAPI`, `FastMCP` is very similar to it.

### MCP Inspector

[link](https://github.com/modelcontextprotocol/inspector)

MCP Inspector is similar to the Postman for the MCP protocol.
It runs via the `npx`.
This repository creates a `task`.
You can spawn `MCP Inspector` using <kbd>cmd + shift + P</kbd> find, `Tasks: Run Task`, then select `RUN MCP Inspector`.

Then you can navigator to http://localhost:6274 to get to the `MCP Inspect` UI.

You can do nothing yet, you will have to run the MCP server first.

## MCP Server

[link](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#what-is-mcp)

First, learn terminology of the MCP server.

- **Resources**: Expose data through Resources (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
- **Tools**: Provide functionality through Tools (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- **Prompts**: Define interaction patterns through Prompts (reusable templates for LLM interactions)

### Stateful VS Stateless

[link](https://gofastmcp.com/deployment/http#horizontal-scaling)

One major decision you should be making before deciding to choose the how your MCP server is going to live in the production is `Horizontal Scaling`.
You should read the manual but in a nutshell, FastMCP is a statefull framework.
However, if you want to put this behind the loadbalancer, it won't work. (even with the sticky session enabled because LLM does not use cookie)
Thus, force you to choose stateless design.

You will lose two MCP features 
- [elicitation](https://gofastmcp.com/servers/elicitation)
- [sampling](https://gofastmcp.com/servers/sampling)

### Transport option

`MCP server` has three transport options.
(1) STDIO
(2) Stream HTTP
(3) SSE (deprecated)

This boilerplate uses (2) Stream HTTP as we intend for this to be a production ready template.

### Running the server

The server will be served with via `uvicorn`.
You can use the vscode task `RUN MCP Server` which will spawn uvicorn server at 0.0.0.0:8000.

Then you can put in the URL in `MCP Inspector` as `http://localhost:8080/mcp`.
Make sure to select `Transportation Type` as `Streamable HTTP` and `Connection Type` as `Direct`.



## MCP Client

[link](https://gofastmcp.com/clients/client)

Just like server situation, the client can consume server in a couple of ways.

```python
# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(server)

# HTTP server
client = Client("https://example.com/mcp")

# Local Python script
client = Client("my_mcp_server.py")
```

In this repository, we will only focus in using client to connect with HTTP MCP server.


### Running the Client

Client is just a normal python file.
To run it, simply use `uv run python src/client/client.py`



