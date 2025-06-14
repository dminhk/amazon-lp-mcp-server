#!/usr/bin/env python3
"""
Amazon Leadership Principles MCP Server

This server provides tools to look up Amazon Leadership Principles
using the Model Context Protocol (MCP).
"""

import json
import os
from typing import Dict

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Amazon LP MCP Server")

# Load data files
def load_data(filename):
    """Load data from a JSON file in the data directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(script_dir), "data", filename)
    
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filename} at {json_path}")
        return {} if filename == "transcripts.json" else {"introduction": "", "principles": []}

# Define the tools

@mcp.tool("amazon_lp")
def amazon_lp() -> Dict:
    """
    Provides the complete Amazon Leadership Principles data.
    
    Returns:
        A dictionary containing the introduction and all Amazon Leadership Principles.
    """
    # Load the data fresh each time to ensure we get the latest version
    lp_data = load_data("amazon-lp.json")
    return lp_data

@mcp.tool("amazon_lp_transcripts")
def amazon_lp_transcripts() -> Dict:
    """
    Provides Andy Jassy's Leadership Principles video transcripts.
    
    Returns:
        A dictionary containing all available leadership principle transcripts.
    """
    # Load the data fresh each time to ensure we get the latest version
    transcript_data = load_data("transcripts.json")
    return transcript_data

if __name__ == "__main__":
    # Run the server
    mcp.run()
