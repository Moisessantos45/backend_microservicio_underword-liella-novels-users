import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from Routers.admin import admin
from Routers.site import site

load_dotenv()

app = FastAPI()
url: str = os.getenv("FRONTEND_HOST")
origins = [url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin, prefix="/api/underword/2.0/admin")
app.include_router(site, prefix="/api/underword/2.0/site")
