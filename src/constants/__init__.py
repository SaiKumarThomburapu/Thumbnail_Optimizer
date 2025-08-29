# Directory for outputs
OUTPUT_DIR = "artifacts"

# File names and extensions
TEMP_VIDEO_PREFIX = "temp_video_"
THUMBNAIL_PREFIX = "thumbnail_"
THUMBNAIL_EXTENSION = ".jpg"

# Validation constants
MAX_FILE_SIZE_MB = 100
ALLOWED_VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov", ".mkv")

# Model configuration
FER_MODEL_CONFIG = {"mtcnn": True}  # For FER initialization

# Frame extraction parameters
HIST_THRESHOLD = 0.85
TOP_K = 5
SAMPLE_DENSITY = 200  # For frame sampling step
SCORING_WEIGHTS = {
    "emotion": 0.5,
    "sharpness": 0.3,
    "face": 0.2
}
SHARPNESS_DIVISOR = 1000
POSITIVE_EMOTIONS = ["happy", "surprise", "neutral"]
