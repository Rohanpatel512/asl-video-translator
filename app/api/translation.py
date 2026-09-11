from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.translation_service import process_frame
from io import BytesIO
from PIL import Image 

translate_router = APIRouter(prefix="/translate", tags=["translate"])

@translate_router.post("/translation/predict")
async def predict(frame: UploadFile):

    contents = await frame.read()

    if not contents:
        raise HTTPException(
            status_code=400, 
            detail="No frame uploaded."
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
