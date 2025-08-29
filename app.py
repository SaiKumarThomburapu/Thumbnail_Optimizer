import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from src.pipeline.full_pipeline import upload_service
from src.logger import logging
from fer import FER
from mtcnn import MTCNN
from src.constants import FER_MODEL_CONFIG
from src.entity.config_entity import ConfigEntity
import src.components.frame_extractor as frame_mod

app = FastAPI(
    title="Thumbnail Optimizer API",
    description="Extract best thumbnail frames from videos using emotion and face detection",
    version="1.0.0"
)

# Ensure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

# In-memory storage
task_data = {}

# Global models
fer_detector = None
face_detector = None

@app.on_event("startup")
async def startup_event():
    global fer_detector, face_detector
    try:
        logging.info("Loading FER...")
        fer_detector = FER(**FER_MODEL_CONFIG)
        logging.info("Loading MTCNN...")
        face_detector = MTCNN()
        # Inject into components
        frame_mod.fer_detector = fer_detector
        frame_mod.face_detector = face_detector
        logging.info("Models loaded and injected into components")
    except Exception as e:
        logging.error(f"Model loading failed: {str(e)}")

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    global fer_detector, face_detector
    if not fer_detector or not face_detector:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    try:
        result = await upload_service(file, task_data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logging.error(f"Video upload error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# @app.get("/get-frame/")
# def get_frame(filename: str):
#     filepath = os.path.join("artifacts", filename)
#     if not os.path.exists(filepath):
#         raise HTTPException(status_code=404, detail="Frame not found")
#     return FileResponse(filepath)

# @app.get("/")
# async def root():
#     return {
#         "message": "Thumbnail Optimizer API is running!",
#         "models_loaded": bool(fer_detector and face_detector),
#         "supported_formats": ConfigEntity().allowed_video_extensions
#     }
