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
