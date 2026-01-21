#!/usr/bin/env python3
"""
Development server script with hot reload enabled.
This script starts MkDocs with live reload functionality.
"""
import os
import subprocess
import sys
from pathlib import Path

def find_venv():
    """Find and return the path to the virtual environment if it exists."""
    script_dir = Path(__file__).parent
    venv_paths = [
        script_dir / "venv",
        script_dir / ".venv",
    ]
    for venv_path in venv_paths:
        if venv_path.exists():
            return venv_path
    return None

def main():
    """Start MkDocs dev server with hot reload."""
    # Try to use mkdocs from virtual environment if it exists
    venv = find_venv()
    if venv:
        # Add venv bin to PATH
        venv_bin = venv / "bin"
        if venv_bin.exists():
            os.environ["PATH"] = str(venv_bin) + os.pathsep + os.environ.get("PATH", "")

    # Check if mkdocs is available
    try:
        result = subprocess.run(
            ["which", "mkdocs"] if sys.platform != "win32" else ["where", "mkdocs"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise FileNotFoundError("mkdocs not found")
    except (FileNotFoundError, subprocess.SubprocessError):
        print("Error: mkdocs not found!")
        print("")
        print("Please install dependencies:")
        print("  1. Create a virtual environment: python3 -m venv venv")
        print("  2. Activate it: source venv/bin/activate")
        print("  3. Install dependencies: pip install -r requirements.txt")
        sys.exit(1)

    print("Starting MkDocs development server with hot reload...")
    print("Open http://127.0.0.1:8000 in your browser")
    print("Changes to markdown files will automatically reload the page")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")

    try:
        # Run mkdocs serve with livereload enabled
        # --livereload enables hot reload (default in newer versions)
        # --watch docs/ explicitly watches the docs directory
        subprocess.run([
            "mkdocs", "serve",
            "--livereload",
            "--watch", "docs/"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)
    except FileNotFoundError:
        print("Error: mkdocs not found. Make sure it's installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
