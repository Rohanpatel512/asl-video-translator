from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from app.services.translation_service import process_frame
from io import BytesIO
from PIL import Image 
from time import time 
from collections import defaultdict

REQUEST_LIMIT = 600
WINDOW_SECONDS = 60
MAX_FRAME_SIZE = 2 * 1024 * 1024 # 2 MB
request_history = defaultdict(list)

translate_router = APIRouter(prefix="/translate", tags=["translate"])

def check_rate_limit(request: Request):
    client_ip = request.client.host
    now = time()

    request_history[client_ip] = [
        timestamp
        for timestamp in request_history[client_ip]
        if now - timestamp < WINDOW_SECONDS
    ]

    if len(request_history[client_ip]) >= REQUEST_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    request_history[client_ip].append(now)

@translate_router.post("/translation/predict")
async def predict(frame: UploadFile, request: Request):

    check_rate_limit(request)

    contents = await frame.read()

    if not contents:
        raise HTTPException(
            status_code=400, 
            detail="No frame uploaded."
        )
    
    if len(contents) > MAX_FRAME_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Frame is too large. Maximum size is 2 MB."
        )


    if frame.content_type not in "image/jpeg":
        raise HTTPException(
            status_code=400,
            detail="The uploaded frame is not a JPEG image."
        )

    try: 
        image = Image.open(BytesIO(contents))
        image.verify() # Verify that the image is valid 

        # Reopen the image 
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded frame is not a valid image."
        )

    data = process_frame(image)

    return data
