"""
Amazon Leadership Principles MCP Server

This package provides tools to look up Amazon Leadership Principles
using the Model Context Protocol (MCP).
"""

from .amazon_lp_mcp_server import mcp

def main():
    """Run the Amazon Leadership Principles MCP server."""
    mcp.run()

__all__ = ["main", "mcp"]
