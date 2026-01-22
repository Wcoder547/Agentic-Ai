# main.py - MCP Math Server for waseem server
"""
Multiplayer MCP Server for math operations.
Exposes math tools via MCP protocol over stdio transport.
"""

import asyncio
import sys
import json
from typing import Any, Dict
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    Resource,
    ListToolsRequestSchema,
    ListToolsResult,
)

# Define math tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage: (part/whole)*100."""
    return (part / whole) * 100

@tool
def solve_equation(x: float, y: float, z: float) -> float:
    """Solve simple equation: x*y + z."""
    return x * y + z

# List of all tools
MATH_TOOLS = [add_numbers, multiply_numbers, calculate_percentage, solve_equation]

async def main():
    """Start MCP server with math tools."""
    
    # Convert LangChain tools to MCP tools
    def tool_to_mcp(tool: Any) -> Tool:
        return Tool(
            name=tool.name,
            description=tool.description,
            inputSchema=tool.args_schema.schema()
        )
    
    tools = [tool_to_mcp(t) for t in MATH_TOOLS]
    
    # MCP Server setup
    server = Server("math-server")
    
    @server.list_tools()
    async def handle_list_tools() -> ListToolsResult:
        return ListToolsResult(tools=tools)
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Resource:
        # Find and execute the tool
        tool = next((t for t in MATH_TOOLS if t.name == name), None)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        
        # Call the tool
        result = tool.invoke(arguments)
        
        return Resource(
            uri="result://math",
            mimeType="text/plain",
            contents=[TextContent(type="text", text=str(result))]
        )
    
    print("🚀 Math MCP Server started on stdio...")
    print("Available tools:", [t.name for t in MATH_TOOLS])
    
    # Start stdio server
    await stdio_server(server)

if __name__ == "__main__":
    asyncio.run(main())
