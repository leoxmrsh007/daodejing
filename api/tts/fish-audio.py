# -*- coding: utf-8 -*-
"""
Fish Audio Serverless Function
"""

import json
import base64
import requests

def handler(event, context):
    """Vercel serverless function for Fish Audio"""

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

    api_key = data.get('api_key')
    text = data.get('text')
    model_id = data.get('model_id')

    if not api_key or not text:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing api_key or text parameter'}),
            'headers': {'Content-Type': 'application/json'}
        }

    try:
        fish_api_url = 'https://api.fish.audio/v1/tts'

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

        response = requests.post(
            fish_api_url,
            headers=headers,
            json=request_body,
            timeout=30
        )

        if response.status_code == 200:
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
                'body': json.dumps({
                    'error': f'Fish Audio API error',
                    'detail': response.text
                }),
                'headers': {'Content-Type': 'application/json'}
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Server error: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }
