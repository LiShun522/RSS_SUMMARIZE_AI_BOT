import os
import logging
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
)
from scheduler import fetch_latest_news
from utils.file_utils import load_data, save_data

# 日誌配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# 載入環境變數
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_ID_FILE = os.path.join(BASE_DIR, "./user_ids.json")

# 初始化用戶 ID 集合
user_ids = load_data(USER_ID_FILE, set())

# Flask 應用
app = Flask(__name__)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# 保存用戶 ID
def save_user_ids():
    save_data(user_ids, USER_ID_FILE)
    logging.info("已儲存用戶 ID。")

# LINE Callback
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_id = event.source.user_id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()
        logging.info(f"新增用戶 ID: {user_id}")
    received_text = event.message.text.strip()

    if received_text == "最新新聞":
        try:
            news_messages = fetch_latest_news(limit=3)
            reply_texts = '\n\n'.join(news_messages) if news_messages else "目前沒有新新聞。"
        except Exception as e:
            logging.error(f"新聞摘要失敗: {e}")
            reply_texts = "抱歉，新聞服務暫時無法使用。"
    else:
        reply_texts = "您可以輸入「最新新聞」來獲取最新資訊。"

    with ApiClient(line_configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            reply_request = ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=reply_texts)]
            )
            line_bot_api.reply_message(reply_request)
            logging.info(f"已回覆用戶 {user_id}。")
        except Exception as e:
            logging.error(f"回覆用戶 {user_id} 時出錯: {e}")

if __name__ == "__main__":
    logging.info("LINE 機器人啟動...")
    app.run(host='0.0.0.0', port=5001)
