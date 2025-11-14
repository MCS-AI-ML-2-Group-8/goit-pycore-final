from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.contact_endpoints import router as contacts_router
from api.notes_endpoints import router as notes_router

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://magic-8.azurewebsites.net"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True, # Allow cookies and authorization headers
    allow_methods=["*"],    # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allow all headers
)
app.include_router(contacts_router)
app.include_router(notes_router)

# Mount assets only if exist
if Path("./app/assets").is_dir():
    app.mount("/assets", StaticFiles(directory="./app/assets"), name="static")
    print("FastAPI: assets mounted")

@app.get("/")
def serve_app():
    return FileResponse("./app/index.html")
