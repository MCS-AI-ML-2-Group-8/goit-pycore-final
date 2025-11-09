import sys
import uvicorn
from api.endpoints import app
from cli.main_loop import launch_main_loop

def main():
    if "--api" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        launch_main_loop()

main()
