from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from dataclasses import dataclass


mcp = FastMCP(
    name="Calculcator-tools",
    version="v0.0.1",
    strict_input_validation=True
    )

@dataclass
class CalculationResult:
    result: int|float

@mcp.tool
async def add(  a: Annotated[int, 
                           Field(description="This is the first number", gt=0)],
                b: Annotated[int, 
                           Field(description="This is the second number", gt=0)]
                ) -> CalculationResult:
    """Adds two integer numbers together."""
    return CalculationResult(result=a + b)

@mcp.tool
async def minus(a: Annotated[int, 
                           Field(description="This is the first number", gt=0)],
                b: Annotated[int, 
                           Field(description="This is the second number", gt=0)]
                ) -> CalculationResult:
    """Minus two integer numbers together."""
    return CalculationResult(result=a - b)

@mcp.tool
async def times(a: Annotated[int, 
                           Field(description="This is the first number", gt=0)],
                b: Annotated[int, 
                           Field(description="This is the second number", gt=0)]
                ) -> CalculationResult:
    """Multiply two integer numbers together."""
    return CalculationResult(result=a * b)

