from fastapi import FastAPI
from api.contact_endpoints import router as contacts_router
from api.notes_endpoints import router as notes_router

app = FastAPI()
app.include_router(contacts_router)
app.include_router(notes_router)

