# -*- coding: utf-8 -*-
"""
TTS 服务 - 语音合成代理服务
支持多语言：普通话、闽南语、粤语、日语、英语等
"""

from typing import Any, Optional, Tuple, Union

import requests
from flask import Response, jsonify, request


class TTSService:
    """TTS 服务基类"""

    def __init__(self) -> None:
        self.timeout = 30

    def validate_request(
        self, required_fields: list[str]
    ) -> Tuple[bool, Optional[str], Optional[Any]]:
        """
        验证请求数据

        Args:
            required_fields: 必需字段列表

        Returns:
            (is_valid, error_message, data)
        """
        data = request.get_json()
        if not data:
            return False, "No JSON data provided", None

        for field in required_fields:
            if not data.get(field):
                return False, f"Missing {field}", None

        return True, None, data


# 多语言语音配置
MULTILANG_VOICES = {
    # 普通话
    "zh-CN": {
        "yunyang": "zh-CN-YunyangNeural",
        "yunjian": "zh-CN-YunjianNeural",
        "yunxi": "zh-CN-YunxiNeural",
        "yunxia": "zh-CN-YunxiaNeural",
        "xiaoxiao": "zh-CN-XiaoxiaoNeural",
        "xiaoyi": "zh-CN-XiaoyiNeural",
    },
    # 粤语
    "zh-HK": {
        "hiumaikai": "zh-HK-HiuMaaiNeural",
        "hiugaai": "zh-HK-HiuGaaiNeural",
        "wanlung": "zh-HK-WanLungNeural",
    },
    # 闽南语（台湾话）
    "zh-TW": {
        "xiaoyi": "zh-TW-HsiaoChenNeural",
        "yunjhe": "zh-TW-YunJheNeural",
        "hsiaoyu": "zh-TW-HsiaoYuNeural",
    },
    # 日语
    "ja-JP": {
        "nanami": "ja-JP-NanamiNeural",
        "keita": "ja-JP-KeitaNeural",
        "shiori": "ja-JP-ShioriNeural",
    },
    # 英语（美式）
    "en-US": {
        "jenny": "en-US-JennyNeural",
        "guy": "en-US-GuyNeural",
        "aria": "en-US-AriaNeural",
    },
    # 英语（英式）
    "en-GB": {
        "sonia": "en-GB-SoniaNeural",
        "ryan": "en-GB-RyanNeural",
    },
}

# 语音名称映射（用于前端显示）
VOICE_NAMES = {
    "zh-CN-YunyangNeural": "普通话 - 云扬（男·沉稳）",
    "zh-CN-YunjianNeural": "普通话 - 云健（男·浑厚）",
    "zh-CN-YunxiNeural": "普通话 - 云希（男·温和）",
    "zh-CN-YunxiaNeural": "普通话 - 云夏（男·沉静）",
    "zh-CN-XiaoxiaoNeural": "普通话 - 晓晓（女·清亮）",
    "zh-CN-XiaoyiNeural": "普通话 - 晓伊（女·柔和）",
    "zh-HK-HiuMaaiNeural": "粤语 - 晓美（女）",
    "zh-HK-HiuGaaiNeural": "粤语 - 晓嘉（女）",
    "zh-HK-WanLungNeural": "粤语 - 云龙（男）",
    "zh-TW-HsiaoChenNeural": "闽南语 - 晓晨（女）",
    "zh-TW-YunJheNeural": "闽南语 - 云哲（男）",
    "zh-TW-HsiaoYuNeural": "闽南语 - 晓雨（女）",
    "ja-JP-NanamiNeural": "日语 - 七海（女）",
    "ja-JP-KeitaNeural": "日语 - 庆太（男）",
    "ja-JP-ShioriNeural": "日语 - 诗织（女）",
    "en-US-JennyNeural": "英语（美）- 珍妮（女）",
    "en-US-GuyNeural": "英语（美）- 盖伊（男）",
    "en-US-AriaNeural": "英语（美）- 阿丽亚（女）",
    "en-GB-SoniaNeural": "英语（英）- 索尼娅（女）",
    "en-GB-RyanNeural": "英语（英）- 瑞恩（男）",
}


class FishAudioService(TTSService):
    """Fish Audio TTS 服务"""

    API_URL = "https://api.fish.audio/v1/tts"

    def synthesize(self) -> Union[Response, Tuple[Response, int]]:
        """
        调用 Fish Audio API 进行语音合成

        Returns:
            Flask Response 对象或 (Response, status_code) 元组
        """
        is_valid, error_msg, data = self.validate_request(["api_key", "text"])
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        assert (
            data is not None
        )  # data is guaranteed to be not None when is_valid is True
        api_key = data.get("api_key")
        text = data.get("text")
        model_id = data.get("model_id")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        request_body = {"text": text, "format": "mp3"}

        if model_id:
            request_body["model_id"] = model_id

        try:
            response = requests.post(
                self.API_URL, headers=headers, json=request_body, timeout=self.timeout
            )

            if response.status_code == 200:
                return Response(
                    response.content,
                    mimetype="audio/mpeg",
                    headers={"Content-Disposition": "attachment; filename=tts.mp3"},
                )
            else:
                return (
                    jsonify(
                        {
                            "error": f"Fish Audio API error: {response.status_code}",
                            "detail": response.text,
                        }
                    ),
                    response.status_code,
                )

        except requests.exceptions.Timeout:
            return jsonify({"error": "Request timeout"}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Request failed: {str(e)}"}), 502
        except Exception as e:
            return jsonify({"error": f"Server error: {str(e)}"}), 500


class EdgeTTSService(TTSService):
    """Edge TTS 服务 (微软免费 TTS)
    支持多语言：普通话、闽南语、粤语、日语、英语等
    """

    API_URL = (
        "https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1"
    )

    def synthesize(self) -> Union[Response, Tuple[Response, int]]:
        """
        调用 Edge TTS API 进行语音合成

        Returns:
            Flask Response 对象或 (Response, status_code) 元组
        """
        is_valid, error_msg, data = self.validate_request(["text"])
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        assert (
            data is not None
        )  # data is guaranteed to not be None when is_valid is True
        text = data.get("text")
        voice = data.get("voice", "zh-CN-YunyangNeural")

        # 根据语音自动检测语言
        lang = self._detect_language_from_voice(voice)

        # 构建 SSML 格式
        ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="{lang}"><voice name="{voice}">{text}</voice></speak>'
        )

        headers = {
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                data=ssml.encode("utf-8"),
                timeout=self.timeout,
            )

            if response.status_code == 200:
                return Response(
                    response.content,
                    mimetype="audio/mpeg",
                    headers={"Content-Disposition": "attachment; filename=tts.mp3"},
                )
            else:
                return (
                    jsonify(
                        {
                            "error": f"Edge TTS error: {response.status_code}",
                            "detail": response.text[:500],
                        }
                    ),
                    response.status_code,
                )

        except requests.exceptions.Timeout:
            return jsonify({"error": "Request timeout"}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Request failed: {str(e)}"}), 502
        except Exception as e:
            return jsonify({"error": f"Server error: {str(e)}"}), 500

    def _detect_language_from_voice(self, voice: str) -> str:
        """
        根据语音名称检测语言

        Args:
            voice: 语音名称（如 zh-CN-XiaoxiaoNeural）

        Returns:
            语言代码（如 zh-CN）
        """
        if voice.startswith("zh-HK"):
            return "zh-HK"  # 粤语
        elif voice.startswith("zh-TW"):
            return "zh-TW"  # 闽南语（台湾话）
        elif voice.startswith("zh-CN"):
            return "zh-CN"  # 普通话
        elif voice.startswith("ja-JP"):
            return "ja-JP"  # 日语
        elif voice.startswith("en-US"):
            return "en-US"  # 英语（美）
        elif voice.startswith("en-GB"):
            return "en-GB"  # 英语（英）
        else:
            return "zh-CN"  # 默认普通话

    def get_available_voices(self) -> dict:
        """
        获取所有可用语音列表

        Returns:
            语音配置字典
        """
        return MULTILANG_VOICES

    def get_voice_name(self, voice_id: str) -> str:
        """
        获取语音显示名称

        Args:
            voice_id: 语音 ID

        Returns:
            显示名称
        """
        return VOICE_NAMES.get(voice_id, voice_id)


# 服务实例
fish_audio_service = FishAudioService()
edge_tts_service = EdgeTTSService()
