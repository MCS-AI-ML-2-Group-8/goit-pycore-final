from fastapi import FastAPI
from api.contact_endpoints import router as contacts_router

app = FastAPI()
app.include_router(contacts_router)
