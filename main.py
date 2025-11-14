import sys

def main():
    if "--api" in sys.argv:
        import uvicorn
        from api.endpoints import app

        uvicorn.run(app, host="0.0.0.0", port=8000)

    elif "--mcp" in sys.argv:
        from llm.tools import mcp

        mcp.run(transport="sse", host="0.0.0.0", port=8001)

    else:
        from cli.main_loop import launch_main_loop

        launch_main_loop()

main()
