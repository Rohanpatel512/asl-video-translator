from fastapi import APIRouter, HTTPException, UploadFile, File
from services.pipeline_services import process_video

translate_router = APIRouter(prefix="/translate", tags=["translate"])

@translate_router.post("/upload")
async def upload_video(file: UploadFile):
    """
    POST request for uploading video file.
    Args
        - File to be uploaded.
    Returns
        - None 
    """
    # Check if file doesn't exist 
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video.")
    
    # Process the uploaded video file
    await process_video(file)
    