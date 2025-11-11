import sys
import uvicorn
from api.endpoints import app
from cli.main_loop import launch_main_loop

def main():
    uvicorn.run(app)

main()
