# RSS_SUMMARIZE_AI_BOT
專案功能 🚀
自動擷取 RSS 新聞

支援多個 RSS 來源，定時抓取最新新聞。
生成新聞摘要

利用 OpenAI 的語言模型自動生成新聞的 3 個重點摘要。
LINE Bot 推送新聞

使用者透過 LINE Bot 輸入「最新新聞」，即可獲取最新 3 篇新聞摘要。
系統定時推送最新新聞給註冊使用者。
容器化部署

使用 Docker 和 Docker Compose 管理並啟動服務。
技術架構 🛠️
程式語言: Python 3.11
框架: Flask
RSS 抓取: Feedparser
新聞摘要: OpenAI (透過 langchain 框架)
定時任務: Schedule
訊息推送: LINE Messaging API
容器化: Docker + Docker Compose
版本控制: Git / GitHub
環境需求 🌐
Python 3.11
Docker 和 Docker Compose
LINE 開發者帳號（取得 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET）
OpenAI API Key（OPENAI_API_KEY）
安裝與執行步驟 🛠️
1. 下載專案
使用 Git 將專案下載到本地：

bash
複製程式碼
git clone https://github.com/LiShun522/RSS_SUMMARIZE_AI_BOT.git
cd RSS_SUMMARIZE_AI_BOT
2. 設定環境變數
在專案根目錄建立 .env 檔案，並填寫以下內容：

plaintext
複製程式碼
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_存取權杖
LINE_CHANNEL_SECRET=你的_LINE_SECRET
OPENAI_API_KEY=你的_OPENAI_API_KEY
3. 安裝依賴套件
bash
複製程式碼
pip install -r requirements.txt
4. 使用 Docker Compose 啟動專案
bash
複製程式碼
docker-compose up --build
5. 使用方式
註冊用戶

加入你的 LINE Bot 並傳送任何訊息，即可註冊為接收新聞的用戶。
查詢最新新聞

輸入「最新新聞」，機器人將回覆最新 3 篇新聞摘要。
定時推播

系統會每分鐘檢查 RSS 更新並自動推送給所有註冊用戶。
