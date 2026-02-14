# -*- coding: utf-8 -*-
"""
服务模块
"""

from services.annotation_service import (DIFFICULT_CHARS,
                                         annotate_difficult_chars)
from services.data_service import DataService
from services.tts_service import edge_tts_service, fish_audio_service

__all__ = [
    "DataService",
    "annotate_difficult_chars",
    "DIFFICULT_CHARS",
    "fish_audio_service",
    "edge_tts_service",
]
