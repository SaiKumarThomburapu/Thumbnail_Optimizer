from src.constants import *

class ConfigEntity:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.temp_video_prefix = TEMP_VIDEO_PREFIX
        self.thumbnail_prefix = THUMBNAIL_PREFIX
        self.thumbnail_extension = THUMBNAIL_EXTENSION
        self.max_file_size_mb = MAX_FILE_SIZE_MB
        self.allowed_video_extensions = ALLOWED_VIDEO_EXTENSIONS
        self.fer_model_config = FER_MODEL_CONFIG
        self.hist_threshold = HIST_THRESHOLD
        self.top_k = TOP_K
        self.sample_density = SAMPLE_DENSITY
        self.scoring_weights = SCORING_WEIGHTS
        self.sharpness_divisor = SHARPNESS_DIVISOR
        self.positive_emotions = POSITIVE_EMOTIONS

class FrameExtractorConfig:
    def __init__(self, config: ConfigEntity):
        self.output_dir = config.output_dir
        self.thumbnail_prefix = config.thumbnail_prefix
        self.thumbnail_extension = config.thumbnail_extension
        self.hist_threshold = config.hist_threshold
        self.top_k = config.top_k
        self.sample_density = config.sample_density
        self.scoring_weights = config.scoring_weights
        self.sharpness_divisor = config.sharpness_divisor
        self.positive_emotions = config.positive_emotions
