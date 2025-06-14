#!/usr/bin/env python3
"""
Amazon Leadership Principles MCP Server

This server provides tools to look up Amazon Leadership Principles
using the Model Context Protocol (MCP).
"""

import json
import os
from typing import List, Dict, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

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

# Load the data
lp_data = load_data("amazon-lp.json")
transcript_data = load_data("transcripts.json")

# Create lookup dictionaries for faster access
principles_by_name = {p["name"].lower(): p for p in lp_data.get("principles", [])}
transcript_keys = {k.replace("-", " ").lower(): (k, v) for k, v in transcript_data.items()}

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

@mcp.tool("ListallAmazonLeadershipPrinciples")
def list_principles() -> LPListResponse:
    """
    List all Amazon Leadership Principles with their descriptions.
    
    Returns:
        A complete list of all Amazon Leadership Principles.
    """
    return LPListResponse(
        introduction=lp_data.get("introduction", ""),
        principles=lp_data.get("principles", [])
    )

@mcp.tool("SearchAmazonLeadershipPrinciples")
def search_principles(query: str = Field(..., description="Search term to find in principle names or descriptions")) -> LPSearchResponse:
    """
    Search for Amazon Leadership Principles by name or description.
    
    Args:
        query: Search term to find in principle names or descriptions
        
    Returns:
        Leadership principles that match the search query.
    """
    query = query.lower()
    matches = [p for p in lp_data.get("principles", []) 
               if query in p["name"].lower() or query in p["description"].lower()]
    
    return LPSearchResponse(matches=matches, query=query)

@mcp.tool("GetaspecificAmazonLeadershipPrinciple")
def get_principle(name: str = Field(..., description="Name of the leadership principle to retrieve")) -> LPGetResponse:
    """
    Get a specific Amazon Leadership Principle by name.
    
    Args:
        name: Name of the leadership principle to retrieve
        
    Returns:
        The requested leadership principle if found.
    """
    name_lower = name.lower()
    
    # Try exact match first
    if name_lower in principles_by_name:
        principle = principles_by_name[name_lower]
        return LPGetResponse(
            principle=principle,
            found=True,
            message=f"Found leadership principle: {principle['name']}"
        )
    
    # Try partial matching
    for principle_name, principle in principles_by_name.items():
        if name_lower in principle_name:
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

@mcp.tool("GetintroductiontoAmazonLeadershipPrinciples")
def get_introduction() -> Dict[str, str]:
    """
    Get the introduction to Amazon Leadership Principles.
    
    Returns:
        The introduction text for Amazon Leadership Principles.
    """
    return {"introduction": lp_data.get("introduction", "")}

@mcp.tool("GettranscriptforaLeadershipPrinciple")
def get_transcript(name: str = Field(..., description="Name of the leadership principle to get the transcript for")) -> TranscriptResponse:
    """
    Get the video transcript for a specific Amazon Leadership Principle.
    
    Args:
        name: Name of the leadership principle to get the transcript for
        
    Returns:
        The transcript for the requested leadership principle if found.
    """
    name_lower = name.lower()
    
    # Try exact match first using our lookup dictionary
    if name_lower in transcript_keys:
        original_key, transcript = transcript_keys[name_lower]
        formatted_name = original_key.replace("-", " ").title()
        return TranscriptResponse(
            principle_name=formatted_name,
            transcript=transcript,
            found=True,
            message=f"Found transcript for: {formatted_name}"
        )
    
    # Try partial matching
    for key_lower, (original_key, transcript) in transcript_keys.items():
        if name_lower in key_lower or key_lower in name_lower:
            formatted_name = original_key.replace("-", " ").title()
            return TranscriptResponse(
                principle_name=formatted_name,
                transcript=transcript,
                found=True,
                message=f"Found transcript for (partial match): {formatted_name}"
            )
    
    return TranscriptResponse(
        principle_name=name,
        transcript="",
        found=False,
        message=f"No transcript found for leadership principle: {name}"
    )

@mcp.tool("Listallavailabletranscripts")
def list_transcripts() -> Dict[str, List[str]]:
    """
    List all available leadership principle transcripts.
    
    Returns:
        A list of all leadership principles that have transcripts available.
    """
    available_transcripts = [k.replace("-", " ").title() for k in transcript_data.keys()]
    return {"available_transcripts": available_transcripts}

@mcp.tool("Searchwithintranscripts")
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
        transcript_lower = transcript.lower()
        if query in transcript_lower:
            formatted_name = principle_name.replace("-", " ").title()
            
            # Find the context around the match
            index = transcript_lower.find(query)
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
    
    return TranscriptSearchResponse(matches=matches, query=query)

if __name__ == "__main__":
    # Run the server
    mcp.run()
