from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.contact_endpoints import router as contacts_router
from api.notes_endpoints import router as notes_router

app = FastAPI()
app.mount("/assets", StaticFiles(directory="./app/assets"), name="static")
app.include_router(contacts_router)
app.include_router(notes_router)

@app.get("/")
def serve_app():
    return FileResponse("./app/index.html")
