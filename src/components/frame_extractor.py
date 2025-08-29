import os
import shutil
import cv2
import numpy as np
import sys
from src.entity.artifacts import FrameExtractionArtifact
from src.entity.config_entity import FrameExtractorConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

# Global models (loaded in app.py)
fer_detector = None
face_detector = None

class FrameExtractor:
    def __init__(self):
        self.config = FrameExtractorConfig(config=ConfigEntity())
        logging.info("FrameExtractor initialized")

    def extract(self, video_path: str) -> FrameExtractionArtifact:
        global fer_detector, face_detector
        try:
            if not fer_detector or not face_detector:
                raise CustomException("Models not loaded", sys)

            # Clean output dir
            shutil.rmtree(self.config.output_dir, ignore_errors=True)
            os.makedirs(self.config.output_dir, exist_ok=True)

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise CustomException("Could not open video", sys)

            frames = []
            frame_scores = []
            prev_hist = None
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            step = max(1, frame_count // self.config.sample_density)

            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_idx % step == 0:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Histogram comparison
                    hist = cv2.calcHist([rgb_frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                    hist = cv2.normalize(hist, hist).flatten()

                    if prev_hist is not None:
                        similarity = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                        if similarity > self.config.hist_threshold:
                            frame_idx += 1
                            continue

                    # Score frame
                    score = self._score_frame(rgb_frame)
                    frames.append(rgb_frame)
                    frame_scores.append(score)
                    prev_hist = hist

                frame_idx += 1

            cap.release()

            if not frames:
                raise CustomException("No frames extracted", sys)

            top_indices = np.argsort(frame_scores)[-self.config.top_k:][::-1]

            thumbnail_paths = []
            for i, idx in enumerate(top_indices):
                filename = f"{self.config.thumbnail_prefix}{i+1}{self.config.thumbnail_extension}"
                filepath = os.path.join(self.config.output_dir, filename)
                cv2.imwrite(filepath, cv2.cvtColor(frames[idx], cv2.COLOR_RGB2BGR))
                thumbnail_paths.append(filepath)

            logging.info(f"Thumbnails extracted successfully: {thumbnail_paths}")
            return FrameExtractionArtifact(thumbnail_paths=thumbnail_paths)

        except Exception as e:
            logging.error(f"Error in frame extraction: {str(e)}")
            return FrameExtractionArtifact(thumbnail_paths=[], error=str(e))

    def _score_frame(self, frame):
        # Emotion detection
        emotions = fer_detector.detect_emotions(frame)
        emotion_score = 0
        if emotions:
            top_emotion = max(emotions[0]["emotions"].items(), key=lambda x: x[1])
            if top_emotion[0] in self.config.positive_emotions:
                emotion_score = top_emotion[1]

        # Face presence
        faces = face_detector.detect_faces(frame)
        face_score = 1 if len(faces) > 0 else 0

        # Sharpness
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        sharpness_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Weighted final score
        final_score = (self.config.scoring_weights["emotion"] * emotion_score) + \
                      (self.config.scoring_weights["sharpness"] * (sharpness_score / self.config.sharpness_divisor)) + \
                      (self.config.scoring_weights["face"] * face_score)
        return final_score
