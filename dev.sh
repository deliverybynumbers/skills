#!/bin/bash
# Development server with hot reload enabled
# This script starts MkDocs with live reload functionality

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists and activate it
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -d "$SCRIPT_DIR/.venv" ]; then
    echo "Activating virtual environment..."
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Check if mkdocs is available
if ! command -v mkdocs &> /dev/null; then
    echo "Error: mkdocs not found!"
    echo ""
    echo "Please install dependencies:"
    echo "  1. Create a virtual environment: python3 -m venv venv"
    echo "  2. Activate it: source venv/bin/activate"
    echo "  3. Install dependencies: pip install -r requirements.txt"
    exit 1
fi

echo "Starting MkDocs development server with hot reload..."
echo "Open http://127.0.0.1:8000 in your browser"
echo "Changes to markdown files will automatically reload the page"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

mkdocs serve --livereload --watch docs/
