import os
import sys
from src.entity.config_entity import ConfigEntity
from src.exceptions import CustomException
from src.logger import logging

async def validate_uploaded_file(upload_file, config: ConfigEntity):
    try:
        ext = os.path.splitext(upload_file.filename)[1].lower()
        if ext not in config.allowed_video_extensions:
            raise CustomException(f"Unsupported file type: {ext}", sys)
        content = await upload_file.read()
        if len(content) > config.max_file_size_mb * 1024 * 1024:
            raise CustomException("File too large", sys)
        return content
    except Exception as e:
        logging.error(f"Error validating file: {str(e)}")
        raise CustomException(e, sys)
