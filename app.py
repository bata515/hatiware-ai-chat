"""Webアプリケーション"""
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from google.generativeai import types as genai_types
import settings
import logging
import os

# ロギング設定
if not settings.DEBUG_MODE:
    logging.basicConfig(level=logging.INFO)

# Gemini API接続
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name=settings.MODEL_NAME,
    system_instruction=settings.SYSTEM_INSTRUCTION
)
chat = model.start_chat()  # チャットセッション開始

app = Flask(__name__)

# 本番環境用設定
if not settings.DEBUG_MODE:
    app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/', methods=['GET', 'HEAD'])
def index():
    """メインページ表示"""
    config = {
        'typewriter_delay': settings.TYPEWRITER_DELAY_MS,
        'avatar_name': settings.AVATAR_NAME,
        'avatar_full_name': settings.AVATAR_FULL_NAME,
        'mouth_animation_interval': settings.MOUTH_ANIMATION_INTERVAL_MS,
        'beep_frequency': settings.BEEP_FREQUENCY_HZ,
        'beep_duration': settings.BEEP_DURATION_MS,
        'beep_volume': settings.BEEP_VOLUME,
        'beep_volume_end': settings.BEEP_VOLUME_END,
        'avatar_image_idle': settings.AVATAR_IMAGE_IDLE,
        'avatar_image_talk': settings.AVATAR_IMAGE_TALK
    }
    return render_template('index.html', config=config)

def trim_history():
    """会話履歴を直近の件数に切り詰める（履歴が無制限に増えるのを防ぐ）"""
    if len(chat.history) > settings.MAX_HISTORY_MESSAGES:
        # userとmodelの発言が対になるよう、偶数件だけ残す
        keep = settings.MAX_HISTORY_MESSAGES - (settings.MAX_HISTORY_MESSAGES % 2)
        chat.history = chat.history[-keep:] if keep else []

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """ユーザー入力を受信しAI応答を返す"""
    # 入力チェック: 不正なリクエストはクライアント側の誤りなので400を返す
    data = request.get_json(silent=True)
    message = data.get('message') if isinstance(data, dict) else None
    if not isinstance(message, str) or not message.strip():
        return jsonify({'error': 'message is required'}), 400
    if len(message) > settings.MAX_MESSAGE_LENGTH:
        return jsonify({'error': 'message is too long'}), 400

    try:
        trim_history()
        response = chat.send_message(
            message,
            request_options={'timeout': settings.GEMINI_TIMEOUT_SEC}
        )
        try:
            text = response.text
        except ValueError as e:
            # 応答に本文が含まれない場合（response.textはValueErrorを送出する）
            app.logger.warning(f"Chat response has no text: {e}")
            text = settings.BLOCKED_RESPONSE_MESSAGE
        return jsonify({'response': text})
    except (genai_types.BlockedPromptException,
            genai_types.StopCandidateException) as e:
        # 安全フィルター等でAIが回答を生成しなかった場合。障害ではないので代替文を返す
        app.logger.warning(f"Chat response blocked: {type(e).__name__}: {e}")
        return jsonify({'response': settings.BLOCKED_RESPONSE_MESSAGE})
    except google_exceptions.ResourceExhausted as e:
        # Gemini APIの利用上限（レート制限）に達した場合
        app.logger.warning(f"Gemini rate limit: {e}")
        return jsonify({'error': 'Too many requests'}), 429
    except Exception as e:
        app.logger.exception(f"Chat API error: {type(e).__name__}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # 開発環境でのみ使用（本番環境ではWSGIサーバーから起動）
    app.run(host='0.0.0.0', debug=settings.DEBUG_MODE, port=settings.SERVER_PORT)