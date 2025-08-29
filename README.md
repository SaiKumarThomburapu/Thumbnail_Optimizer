# Thumbnail Optimizer API

## Overview

Thumbnail Optimizer is a production-ready API service designed to extract the most engaging thumbnail frames from uploaded videos. Leveraging machine learning models for facial emotion recognition (FER), face detection (MTCNN), and image sharpness analysis, the system scores and ranks frames to select the top candidates. This project follows a modular MLOps (Machine Learning Operations) structure inspired by best practices for scalability, reproducibility, and maintainability.

Key objectives:
- Automate thumbnail generation for videos, prioritizing frames with positive emotions (e.g., happy, surprise), faces, and high sharpness.
- Ensure efficient processing with temporary file handling and automatic cleanup to minimize resource usage.
- Provide a RESTful API for easy integration into web applications, content platforms, or media workflows.

This structure emphasizes separation of concerns, configuration-driven parameters, and global model loading for performance. It is built on FastAPI for high-performance asynchronous API serving.

## Features

- **Intelligent Frame Selection**: Samples frames, filters duplicates using histogram comparison, and scores based on emotion, face presence, and sharpness.
- **MLOps Best Practices**:
  - Modular components for extraction and scoring.
  - Centralized configuration via constants.
  - Artifact dataclasses for structured outputs.
  - Pipeline orchestration with task tracking and error handling.
  - Global model initialization on startup to reduce latency.
- **Temporary Storage**: Videos are stored in temporary directories and deleted immediately after processing (on success or failure).
- **API Endpoints**:
  - Upload videos and receive top thumbnail paths.
  - Fetch generated thumbnails.
- **Configurable Parameters**: Easily adjust scoring weights, thresholds, and more via constants.
- **Error Handling**: Custom exceptions, logging, and validation for file types/size.

## Architecture

The project adheres to a clean MLOps directory structure:

Thumbnail_Optimizer_MLOps/
├── src/
│ ├── components/ # Core processing classes (e.g., frame_extractor.py)
│ ├── constants/ # Centralized constants (e.g., init.py)
│ ├── entity/ # Data models (e.g., artifacts.py, config_entity.py)
│ ├── exceptions/ # Custom exceptions
│ ├── logger/ # Logging utilities
│ ├── pipeline/ # Orchestration logic (e.g., full_pipeline.py)
│ └── utils/ # Helpers (e.g., io_utils.py)
├── app.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── Dockerfile # (Optional) For containerization
├── .gitignore # Git ignore file
└── README.md # This file

text

- **Components**: Handle specific tasks like frame extraction and scoring.
- **Pipeline**: Manages the end-to-end workflow, including validation, temporary storage, processing, and cleanup.
- **Models**: FER and MTCNN are loaded globally in `app.py` and injected into components for reuse.

## Installation

### Prerequisites
- Python 3.10
- pip (Python package manager)
- Hardware: GPU recommended for faster model inference (FER/MTCNN).

### Steps
1. Clone the repository:
git clone https://github.com/your-username/thumbnail_optimizer.git
cd thumbnail_optimizer

text

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

text

3. Install dependencies:
pip install -r requirements.txt

## Usage

### Running the API
Start the server:
uvicorn app:app --reload --host 0.0.0.0 --port 8000

text
The API will be available at `http://localhost:8000`.

### API Endpoints

- **POST /upload-video/**: Upload a video for processing.
  - Request: Multipart form with `file` (video file, max 100MB, supported: .mp4, .avi, .mov, .mkv).
  - Response: JSON with task_id, status, and thumbnail_paths (e.g., ["artifacts/thumbnail_1.jpg"]).
  - Example (using curl):
    ```
    curl -X POST "http://localhost:8000/upload-video/" -F "file=@/path/to/video.mp4"
    ```
  - Processing: Video is temporarily stored, frames are extracted/scored, top 5 are saved to "artifacts/", temp files are deleted.

### Configuration
All parameters are defined in `src/constants/__init__.py`. Key examples:
- `TOP_K = 5`: Number of top thumbnails to extract.
- `HIST_THRESHOLD = 0.85`: Similarity threshold for skipping duplicate frames.
- `POSITIVE_EMOTIONS = ["happy", "surprise"]`: Emotions that contribute to scoring (expand as needed).
- `SCORING_WEIGHTS`: Adjust weights for emotion, sharpness, and face presence.

Modify and restart the server for changes to take effect.

### Example Workflow
1. Upload a video via POST request.
2. Receive task_id and thumbnail_paths in response.
3. Download thumbnails using GET requests.
4. Artifacts are stored in "artifacts/" (cleaned per upload).

## How It Works (Technical Details)

1. **Upload Handling**: Validates file, saves to temp dir using `tempfile.mkdtemp()`.
2. **Frame Extraction**:
   - Samples frames (up to ~200 based on video length).
   - Filters similar frames via histogram correlation.
   - Scores each: Emotion (FER), Face (MTCNN), Sharpness (Laplacian).
   - Selects and saves top-scoring frames.
3. **Cleanup**: Deletes temp dir immediately after processing.
4. **Models**: Loaded on startup for efficiency; supports CPU/GPU.

For more on the scoring logic, see `src/components/frame_extractor.py`.

## Performance Considerations
- **Scalability**: Use a task queue (e.g., Celery) for high-volume uploads.
- **Optimization**: Models can be resource-intensive; deploy on GPU-enabled servers.
- **Limitations**: Processes videos synchronously; add async workers for concurrency.
---
For questions or customizations, open an issue or contact the maintainer. This README was last updated on August 29, 2025.
