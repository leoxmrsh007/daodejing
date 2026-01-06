# -*- coding: utf-8 -*-
"""
Edge TTS Serverless Function
"""

import json
import base64
import requests

def handler(event, context):
    """Vercel serverless function for Edge TTS"""

    # 只处理POST请求
    method = event.get('httpMethod', event.get('method', 'GET'))
    if method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # 解析请求体
    try:
        body_data = event.get('body', '')
        if isinstance(body_data, str):
            data = json.loads(body_data) if body_data else {}
        else:
            data = body_data
    except:
        data = {}

    text = data.get('text')
    voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')

    if not text:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing text parameter'}),
            'headers': {'Content-Type': 'application/json'}
        }

    try:
        # 构建SSML格式
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN"><voice name="{voice}">{text}</voice></speak>'

        # Edge TTS API端点
        edge_tts_url = 'https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'

        headers = {
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.post(
            edge_tts_url,
            headers=headers,
            data=ssml.encode('utf-8'),
            timeout=30
        )

        if response.status_code == 200:
            # 将音频数据转为base64
            audio_base64 = base64.b64encode(response.content).decode('utf-8')
            return {
                'statusCode': 200,
                'body': audio_base64,
                'headers': {'Content-Type': 'audio/mpeg'},
                'isBase64Encoded': True
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': f'Edge TTS error: {response.status_code}'}),
                'headers': {'Content-Type': 'application/json'}
            }

    except requests.exceptions.Timeout:
        return {
            'statusCode': 504,
            'body': json.dumps({'error': 'Request timeout'}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Server error: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }
