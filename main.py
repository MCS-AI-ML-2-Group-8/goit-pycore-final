"""
Entry point for the contact management assistant application.

This module provides a dual-mode launcher that can run either:
- CLI mode: Interactive command-line interface (default)
- API mode: REST API server (activated with --api flag)

Usage:
    python main.py           # Launch CLI mode
    python main.py --api     # Launch API server on http://127.0.0.1:8000
"""

import sys

def main():
    if "--api" in sys.argv:
        import uvicorn
        from api.endpoints import app

        uvicorn.run(app, host="0.0.0.0", port=8000)

    else:
        from cli.main_loop import launch_main_loop

        launch_main_loop()

main()
