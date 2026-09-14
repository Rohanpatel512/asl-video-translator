from fastapi import FastAPI
from app.api.translation import translate_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.config import (
    HAND_MODEL_REPO,
    HAND_MODEL_FILENAME,
    HAND_DETECTION_CONFIDENCE,
    CORS_ORIGINS
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(translate_router)

app.mount(
    "/assets",
    StaticFiles(directory="app/frontend/assets"),
    name="assets"
)