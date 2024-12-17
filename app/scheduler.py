import os
import logging
import time
import feedparser
import schedule
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
)
from utils.file_utils import load_data, save_data

# 日誌配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# 載入環境變數
load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUSHED_TITLES_FILE = os.path.join(BASE_DIR, "./pushed_titles.json")
USER_ID_FILE = os.path.join(BASE_DIR, "./user_ids.json")

# RSS 源
RSS_URLS = {
    "https://tw.stock.yahoo.com/rss?category=intl-markets": "Yahoo 國際市場",
    "https://www.moneydj.com/KMDJ/RssCenter.aspx?svc=NR&fno=1&arg=MB010000": "MoneyDJ 財經新聞",
    "https://feeds.feedburner.com/ettoday/finance": "ETtoday 財經新聞",
}

# OpenAI 客戶端
openai_client = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.3, max_tokens=150)

# 生成摘要
def summarize_content(title, content):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "請根據以下新聞標題與內容生成 3 個重點摘要：\n標題: {title}\n內容: {content}")
    ])
    try:
        content = content or "新聞內容暫無詳細描述。"
        runnable = prompt | openai_client
        response = runnable.invoke({"title": title, "content": content})
        logging.info(f"成功生成摘要: {title}")
        return response.content.strip()
    except Exception as e:
        logging.error(f"摘要生成失敗: {e}")
        return "抱歉，無法生成摘要。"

# 抓取 RSS 並返回最近新聞
def fetch_latest_news(limit=3):
    messages = []
    pushed_titles = load_data(PUSHED_TITLES_FILE, set())
    new_pushed_titles = set()

    for rss_url, source_name in RSS_URLS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            logging.warning(f"RSS 來源無法解析或無新聞: {rss_url}")
            continue

        for entry in feed.entries[:limit]:
            if entry.title in pushed_titles:
                continue  # 跳過已推送的新聞

            summary = summarize_content(entry.title, entry.description)
            message = f"📰 標題: {entry.title}\n🔍 摘要:\n{summary}\n🔗 閱讀更多: {entry.link}\n📡 來源: {source_name}"
            messages.append(message)
            new_pushed_titles.add(entry.title)

    # 更新 pushed_titles.json
    if new_pushed_titles:
        pushed_titles.update(new_pushed_titles)
        save_data(pushed_titles, PUSHED_TITLES_FILE)
        logging.info("成功更新已推送的新聞標題。")

    return messages

# 推送 RSS
def get_and_push_rss():
    user_ids = load_data(USER_ID_FILE, set())  # 每次讀取最新用戶 ID

    if not user_ids:
        logging.info("目前沒有註冊的用戶，無法推送新聞。")
        return

    logging.info(f"當前註冊的用戶 ID: {', '.join(user_ids)}")
    messages = fetch_latest_news()
    if not messages:
        logging.info("沒有新新聞可推送。")
        return

    # 開始推送
    with ApiClient(Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)) as api_client:
        line_bot_api = MessagingApi(api_client)
        for user_id in user_ids:
            for message in messages:
                try:
                    push_request = PushMessageRequest(to=user_id, messages=[TextMessage(text=message)])
                    line_bot_api.push_message(push_request)
                    logging.info(f"成功推送新聞給用戶 {user_id}")
                except Exception as e:
                    logging.error(f"推送新聞給用戶 {user_id} 失敗: {e}")

# 定時任務
schedule.every(1).minutes.do(get_and_push_rss)

if __name__ == "__main__":
    logging.info("新聞推送定時任務啟動...")
    get_and_push_rss()  # 初次執行時推送一次
    while True:
        schedule.run_pending()
        time.sleep(1)
