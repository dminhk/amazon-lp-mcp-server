# Amazon Leadership Principles MCP Server

This is a Model Context Protocol (MCP) server that provides tools to look up Amazon Leadership Principles and their video transcripts.

## Installation

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### Running the server

```bash
# Run the server
amazon-lp-mcp-server
```

Or you can run it directly:

```bash
python main.py
```

### Using with Amazon Q CLI

To use this MCP server with Amazon Q CLI, add it to your Q CLI configuration:

1. Create or edit your Q CLI configuration file (typically located at `~/.q/config.json`):

```json
{
  "mcpServers": {
    "AmazonLP": {
      "command": "amazon-lp-mcp-server"
    }
  }
}
```

2. For development or using directly from GitHub:

```json
{
  "mcpServers": {
    "AmazonLP": {
      "command": "uvx",
      "args": [
        "git+https://github.com/dminhk/amazon-lp-mcp-server/"
      ]
    }
  }
}
```

3. Start a conversation with Amazon Q CLI and use the MCP server:

```bash
q chat
```

You can now ask Amazon Q about Amazon Leadership Principles, and it will use the tools provided by this MCP server to give you accurate information.

### Available Tools

The server provides the following simplified tools:

1. **amazon_lp** - Provides the complete Amazon Leadership Principles data from amazon-lp.json.

2. **amazon_lp_transcripts** - Provides Andy Jassy's Leadership Principles video transcripts from transcripts.json.

## Example Queries

When using with Amazon Q CLI, you can ask questions like:

- "What are all the Amazon Leadership Principles?"
- "Tell me about the Customer Obsession principle"
- "Search for principles related to innovation"
- "Show me the transcript for Earn Trust"
- "Which leadership principles have transcripts available?"
- "Search transcripts for mentions of 'long-term'"

## Data Sources

The server uses the following data sources:

- `amazon-lp.json` - Contains all Amazon Leadership Principles and their descriptions
- `transcripts.json` - Contains Andy Jassy's video transcripts for each leadership principle

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request
