import os
import sys
import uuid
import tempfile
import shutil
from fastapi import UploadFile
from src.entity.config_entity import ConfigEntity
from src.components.frame_extractor import FrameExtractor
from src.utils.io_utils import validate_uploaded_file
from src.logger import logging
from src.exceptions import CustomException

async def upload_service(video: UploadFile, task_data: dict):
    try:
        base_config = ConfigEntity()
        task_id = uuid.uuid4().hex
        video_name = os.path.splitext(video.filename)[0]  # Get video name without extension

        # Validate and read file
        file_content = await validate_uploaded_file(video, base_config)

        # Create temp dir and save video
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, f"{base_config.temp_video_prefix}{uuid.uuid4()}{os.path.splitext(video.filename)[1]}")
        with open(video_path, "wb") as buffer:
            buffer.write(file_content)

        # Initialize task
        task_data[task_id] = {
            "status": "processing",
            "thumbnail_paths": None,
            "error": None,
            "temp_dir": temp_dir
        }

        logging.info(f"Task {task_id} processing started for video: {video_name}")

        # Process synchronously
        process_task(task_id, task_data, video_name)

        result = task_data[task_id]
        if result["status"] == "failed":
            raise CustomException(result["error"], sys)

        logging.info(f"Task {task_id} completed")
        return {
            "task_id": task_id,
            "status": result["status"],
            "message": "Processing completed",
            "thumbnail_paths": result["thumbnail_paths"]
        }

    except Exception as e:
        if task_id in task_data and "temp_dir" in task_data[task_id]:
            shutil.rmtree(task_data[task_id]["temp_dir"], ignore_errors=True)
        if task_id in task_data:
            task_data[task_id]["status"] = "failed"
            task_data[task_id]["error"] = str(e)
        raise CustomException(e, sys)

def process_task(task_id: str, task_data: dict, video_name: str):
    try:
        if task_id not in task_data:
            raise CustomException(f"Task not found: {task_id}", sys)

        temp_dir = task_data[task_id]["temp_dir"]
        video_path = next((os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.startswith(ConfigEntity().temp_video_prefix)), None)
        if not video_path:
            raise CustomException("Temporary video not found", sys)

        # Extract frames
        extractor = FrameExtractor()
        frame_artifact = extractor.extract(video_path)
        if frame_artifact.error:
            task_data[task_id]["status"] = "failed"
            task_data[task_id]["error"] = frame_artifact.error
            return

        # Update task data
        task_data[task_id].update({
            "status": "completed",
            "thumbnail_paths": frame_artifact.thumbnail_paths
        })

        # Cleanup
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

    except Exception as e:
        if "temp_dir" in task_data[task_id]:
            shutil.rmtree(task_data[task_id]["temp_dir"], ignore_errors=True)
        task_data[task_id]["status"] = "failed"
        task_data[task_id]["error"] = str(e)
        logging.error(f"Task {task_id} failed: {str(e)}")
        raise  
