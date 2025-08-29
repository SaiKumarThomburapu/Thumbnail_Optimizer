from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FrameExtractionArtifact:
    thumbnail_paths: List[str]
    error: Optional[str] = None
