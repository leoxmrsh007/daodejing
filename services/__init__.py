# -*- coding: utf-8 -*-
"""
服务模块
"""

from services.data_service import DataService
from services.annotation_service import annotate_difficult_chars, DIFFICULT_CHARS
from services.tts_service import fish_audio_service, edge_tts_service

__all__ = [
    'DataService',
    'annotate_difficult_chars',
    'DIFFICULT_CHARS',
    'fish_audio_service',
    'edge_tts_service',
]
