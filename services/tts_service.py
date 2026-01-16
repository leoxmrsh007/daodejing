# -*- coding: utf-8 -*-
"""
TTS 服务 - 语音合成代理服务
"""

import requests
from flask import request, jsonify, Response


class TTSService:
    """TTS 服务基类"""

    def __init__(self):
        self.timeout = 30

    def validate_request(self, required_fields: list) -> tuple:
        """
        验证请求数据

        Args:
            required_fields: 必需字段列表

        Returns:
            (is_valid, error_message, data)
        """
        data = request.get_json()
        if not data:
            return False, 'No JSON data provided', None

        for field in required_fields:
            if not data.get(field):
                return False, f'Missing {field}', None

        return True, None, data


class FishAudioService(TTSService):
    """Fish Audio TTS 服务"""

    API_URL = 'https://api.fish.audio/v1/tts'

    def synthesize(self) -> Response:
        """
        调用 Fish Audio API 进行语音合成

        Returns:
            Flask Response 对象
        """
        is_valid, error_msg, data = self.validate_request(['api_key', 'text'])
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        api_key = data.get('api_key')
        text = data.get('text')
        model_id = data.get('model_id')

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        request_body = {
            'text': text,
            'format': 'mp3'
        }

        if model_id:
            request_body['model_id'] = model_id

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=request_body,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return Response(
                    response.content,
                    mimetype='audio/mpeg',
                    headers={
                        'Content-Disposition': 'attachment; filename=tts.mp3'
                    }
                )
            else:
                return jsonify({
                    'error': f'Fish Audio API error: {response.status_code}',
                    'detail': response.text
                }), response.status_code

        except requests.exceptions.Timeout:
            return jsonify({'error': 'Request timeout'}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Request failed: {str(e)}'}), 502
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500


class EdgeTTSService(TTSService):
    """Edge TTS 服务 (微软免费 TTS)"""

    API_URL = 'https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'

    def synthesize(self) -> Response:
        """
        调用 Edge TTS API 进行语音合成

        Returns:
            Flask Response 对象
        """
        is_valid, error_msg, data = self.validate_request(['text'])
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        text = data.get('text')
        voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')

        # 构建 SSML 格式
        ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="zh-CN"><voice name="{voice}">{text}</voice></speak>'
        )

        headers = {
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                data=ssml.encode('utf-8'),
                timeout=self.timeout
            )

            if response.status_code == 200:
                return Response(
                    response.content,
                    mimetype='audio/mpeg',
                    headers={
                        'Content-Disposition': 'attachment; filename=tts.mp3'
                    }
                )
            else:
                return jsonify({
                    'error': f'Edge TTS error: {response.status_code}',
                    'detail': response.text[:500]
                }), response.status_code

        except requests.exceptions.Timeout:
            return jsonify({'error': 'Request timeout'}), 504
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Request failed: {str(e)}'}), 502
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500


# 服务实例
fish_audio_service = FishAudioService()
edge_tts_service = EdgeTTSService()
