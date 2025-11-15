from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.contact_endpoints import router as contacts_router
from api.notes_endpoints import router as notes_router
from api.chat_endpoints import router as chat_router
from llm.tools import mcp

# CORS
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://magic-8.azurewebsites.net"
]

# MCP server
mcp_app = mcp.http_app("/", transport="sse")

app = FastAPI(lifespan=mcp_app.lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True, # Allow cookies and authorization headers
    allow_methods=["*"],    # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allow all headers
)
app.include_router(contacts_router)
app.include_router(notes_router)
app.include_router(chat_router)

# MCP server
app.mount("/mcp", mcp_app)

# Frontend
@app.get("/", include_in_schema=False)
def serve_app():
    return FileResponse("./app/index.html")

# Mount assets only if exist
if Path("./app/assets").is_dir():
    app.mount("/", StaticFiles(directory="./app/"), name="static")
    print("FastAPI: assets mounted")
