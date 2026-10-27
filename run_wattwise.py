"""Start WattWise using the Python interpreter selected in VS Code.

Examples:
    python run_wattwise.py
    python run_wattwise.py --port 8502
"""

import argparse
from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parent
APP_PATH = PROJECT_DIR / "app.py"


def build_streamlit_command(port=8501):
    """Build the command as a list so Windows paths with spaces work safely."""
    if not 1024 <= port <= 65535:
        raise ValueError("Port must be between 1024 and 65535")
    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP_PATH),
        "--server.headless",
        "true",
        "--server.port",
        str(port),
        "--browser.gatherUsageStats",
        "false",
    ]


def main():
    parser = argparse.ArgumentParser(description="Run the WattWise Streamlit application")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()

    if not APP_PATH.exists():
        raise FileNotFoundError(f"Cannot find {APP_PATH}")

    command = build_streamlit_command(args.port)
    print("Starting WattWise...")
    print(f"Open http://localhost:{args.port} in your browser if it does not open automatically.")
    print("Press Ctrl+C in the terminal to stop the server.")

    try:
        subprocess.run(command, cwd=PROJECT_DIR, check=True)
    except KeyboardInterrupt:
        print("\nWattWise stopped by the user.")
    except subprocess.CalledProcessError as error:
        print("\nWattWise could not start.")
        print("Activate the virtual environment and run: python -m pip install -r requirements.txt")
        raise SystemExit(error.returncode) from error


if __name__ == "__main__":
    main()
