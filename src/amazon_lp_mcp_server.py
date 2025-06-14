#!/usr/bin/env python3
"""
Amazon Leadership Principles MCP Server

This server provides tools to look up Amazon Leadership Principles
using the Model Context Protocol (MCP).
"""

import json
import os
from typing import List, Optional, Dict, Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Create an MCP server
mcp = FastMCP("Amazon LP MCP Server")

# Load the Amazon Leadership Principles data
def load_lp_data():
    """Load the Amazon Leadership Principles data from the JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(script_dir), "amazon-lp.json")
    
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find amazon-lp.json at {json_path}")
        return {"introduction": "", "principles": []}

# Load the transcripts data
def load_transcript_data():
    """Load the transcript data from the JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(script_dir), "transcripts.json")
    
    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find transcripts.json at {json_path}")
        return {}

# Load the data
lp_data = load_lp_data()
transcript_data = load_transcript_data()

# Define models for the tools
class LPPrinciple(BaseModel):
    """A single Amazon Leadership Principle."""
    name: str = Field(..., description="The name of the leadership principle")
    description: str = Field(..., description="The description of the leadership principle")

class LPListResponse(BaseModel):
    """Response model for listing all leadership principles."""
    introduction: str = Field(..., description="Introduction to Amazon Leadership Principles")
    principles: List[LPPrinciple] = Field(..., description="List of all leadership principles")

class LPSearchResponse(BaseModel):
    """Response model for searching leadership principles."""
    matches: List[LPPrinciple] = Field(..., description="List of matching leadership principles")
    query: str = Field(..., description="The search query used")

class LPGetResponse(BaseModel):
    """Response model for getting a specific leadership principle."""
    principle: Optional[LPPrinciple] = Field(None, description="The requested leadership principle")
    found: bool = Field(..., description="Whether the principle was found")
    message: str = Field(..., description="Status message")

class TranscriptResponse(BaseModel):
    """Response model for getting a transcript."""
    principle_name: str = Field(..., description="The name of the leadership principle")
    transcript: str = Field(..., description="The transcript text")
    found: bool = Field(..., description="Whether the transcript was found")
    message: str = Field(..., description="Status message")

class TranscriptSearchResponse(BaseModel):
    """Response model for searching transcripts."""
    matches: List[Dict[str, str]] = Field(..., description="List of matching transcripts with principle names")
    query: str = Field(..., description="The search query used")

# Define the tools

@mcp.tool("List all Amazon Leadership Principles")
def list_principles() -> LPListResponse:
    """
    List all Amazon Leadership Principles with their descriptions.
    
    Returns:
        A complete list of all Amazon Leadership Principles.
    """
    return LPListResponse(
        introduction=lp_data["introduction"],
        principles=lp_data["principles"]
    )

@mcp.tool("Search Amazon Leadership Principles")
def search_principles(query: str = Field(..., description="Search term to find in principle names or descriptions")) -> LPSearchResponse:
    """
    Search for Amazon Leadership Principles by name or description.
    
    Args:
        query: Search term to find in principle names or descriptions
        
    Returns:
        Leadership principles that match the search query.
    """
    query = query.lower()
    matches = []
    
    for principle in lp_data["principles"]:
        if (query in principle["name"].lower() or 
            query in principle["description"].lower()):
            matches.append(principle)
    
    return LPSearchResponse(
        matches=matches,
        query=query
    )

@mcp.tool("Get a specific Amazon Leadership Principle")
def get_principle(name: str = Field(..., description="Name of the leadership principle to retrieve")) -> LPGetResponse:
    """
    Get a specific Amazon Leadership Principle by name.
    
    Args:
        name: Name of the leadership principle to retrieve
        
    Returns:
        The requested leadership principle if found.
    """
    name_lower = name.lower()
    
    for principle in lp_data["principles"]:
        if principle["name"].lower() == name_lower:
            return LPGetResponse(
                principle=principle,
                found=True,
                message=f"Found leadership principle: {principle['name']}"
            )
    
    # Try partial matching if exact match fails
    for principle in lp_data["principles"]:
        if name_lower in principle["name"].lower():
            return LPGetResponse(
                principle=principle,
                found=True,
                message=f"Found leadership principle (partial match): {principle['name']}"
            )
    
    return LPGetResponse(
        principle=None,
        found=False,
        message=f"No leadership principle found with name: {name}"
    )

@mcp.tool("Get introduction to Amazon Leadership Principles")
def get_introduction() -> Dict[str, str]:
    """
    Get the introduction to Amazon Leadership Principles.
    
    Returns:
        The introduction text for Amazon Leadership Principles.
    """
    return {
        "introduction": lp_data["introduction"]
    }

@mcp.tool("Get transcript for a Leadership Principle")
def get_transcript(name: str = Field(..., description="Name of the leadership principle to get the transcript for")) -> TranscriptResponse:
    """
    Get the video transcript for a specific Amazon Leadership Principle.
    
    Args:
        name: Name of the leadership principle to get the transcript for
        
    Returns:
        The transcript for the requested leadership principle if found.
    """
    # Normalize the name for matching
    name_lower = name.lower()
    
    # Try to find an exact match first
    for principle_name, transcript in transcript_data.items():
        principle_key = principle_name.replace("-", " ")
        if principle_key.lower() == name_lower:
            return TranscriptResponse(
                principle_name=principle_name.replace("-", " ").title(),
                transcript=transcript,
                found=True,
                message=f"Found transcript for: {principle_name.replace('-', ' ').title()}"
            )
    
    # Try partial matching if exact match fails
    for principle_name, transcript in transcript_data.items():
        principle_key = principle_name.replace("-", " ")
        if name_lower in principle_key.lower():
            return TranscriptResponse(
                principle_name=principle_name.replace("-", " ").title(),
                transcript=transcript,
                found=True,
                message=f"Found transcript for (partial match): {principle_name.replace('-', ' ').title()}"
            )
    
    # Try to match against the principle names in lp_data
    for principle in lp_data["principles"]:
        if principle["name"].lower() == name_lower:
            # Try to find a matching transcript
            for principle_name, transcript in transcript_data.items():
                principle_key = principle_name.replace("-", " ")
                if principle_key.lower() in principle["name"].lower() or principle["name"].lower() in principle_key.lower():
                    return TranscriptResponse(
                        principle_name=principle["name"],
                        transcript=transcript,
                        found=True,
                        message=f"Found transcript for: {principle['name']}"
                    )
    
    return TranscriptResponse(
        principle_name=name,
        transcript="",
        found=False,
        message=f"No transcript found for leadership principle: {name}"
    )

@mcp.tool("List all available transcripts")
def list_transcripts() -> Dict[str, List[str]]:
    """
    List all available leadership principle transcripts.
    
    Returns:
        A list of all leadership principles that have transcripts available.
    """
    available_transcripts = []
    
    for principle_name in transcript_data.keys():
        formatted_name = principle_name.replace("-", " ").title()
        available_transcripts.append(formatted_name)
    
    return {
        "available_transcripts": available_transcripts
    }

@mcp.tool("Search within transcripts")
def search_transcripts(query: str = Field(..., description="Search term to find in transcripts")) -> TranscriptSearchResponse:
    """
    Search for a term within all leadership principle transcripts.
    
    Args:
        query: Search term to find in transcripts
        
    Returns:
        Leadership principles with transcripts that match the search query.
    """
    query = query.lower()
    matches = []
    
    for principle_name, transcript in transcript_data.items():
        if query in transcript.lower():
            formatted_name = principle_name.replace("-", " ").title()
            # Find the context around the match (up to 100 characters before and after)
            index = transcript.lower().find(query)
            start = max(0, index - 100)
            end = min(len(transcript), index + len(query) + 100)
            
            # Get the context and add ellipsis if needed
            context = transcript[start:end]
            if start > 0:
                context = "..." + context
            if end < len(transcript):
                context = context + "..."
            
            matches.append({
                "principle_name": formatted_name,
                "context": context
            })
    
    return TranscriptSearchResponse(
        matches=matches,
        query=query
    )

if __name__ == "__main__":
    # Run the server
    mcp.run()
