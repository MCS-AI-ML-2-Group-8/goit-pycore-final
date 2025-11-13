import sys
import uvicorn
from api.endpoints import app
from cli.main_loop import launch_main_loop
from llm.tools import mcp

def main():
    if "--api" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif "--mcp" in sys.argv:
        mcp.run(transport="sse", host="0.0.0.0", port=8001)
    else:
        launch_main_loop()

main()
