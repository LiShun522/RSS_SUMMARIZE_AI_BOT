# RSS Summary Bot 📄🤖

這是一個自動推播新聞摘要的機器人專案，透過 **LINE Bot** 傳送最新新聞，並結合 **OpenAI** 生成重點摘要，讓使用者可以快速掌握最新資訊。

---

## 專案功能 🚀

1. **自動擷取 RSS 新聞**  
   - 支援多個 RSS 來源，定時抓取最新新聞。

2. **生成新聞摘要**  
   - 利用 OpenAI 的語言模型自動生成新聞的 3 個重點摘要。

3. **LINE Bot 推送新聞**  
   - 使用者透過 LINE Bot 輸入「最新新聞」，即可獲取最新 3 篇新聞摘要。  
   - 系統定時推送最新新聞給註冊使用者。

4. **容器化部署**  
   - 使用 Docker 和 Docker Compose 管理並啟動服務。

---

## 技術架構 🛠️

- **程式語言**: Python 3.11
- **框架**: Flask
- **RSS 抓取**: Feedparser
- **新聞摘要**: OpenAI (透過 `langchain` 框架)
- **定時任務**: Schedule
- **訊息推送**: LINE Messaging API
- **容器化**: Docker + Docker Compose
- **版本控制**: Git / GitHub

---

## 環境需求 🌐

- **Python 3.11**
- **Docker** 和 **Docker Compose**
- **LINE 開發者帳號**（取得 `LINE_CHANNEL_ACCESS_TOKEN` 和 `LINE_CHANNEL_SECRET`）
- **OpenAI API Key**（`OPENAI_API_KEY`）

---

## 安裝與執行步驟 🛠️

### 1. 下載專案

使用 Git 將專案下載到本地：

```bash
git clone https://github.com/LiShun522/RSS_SUMMARIZE_AI_BOT.git
cd RSS_SUMMARIZE_AI_BOT
```
## 設定環境變數
在專案根目錄建立 .env 檔案，並填寫以下內容：
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_存取權杖
LINE_CHANNEL_SECRET=你的_LINE_SECRET
OPENAI_API_KEY=你的_OPENAI_API_KEY

## 安裝依賴套件
```bash
pip install -r requirements.txt
```
## 使用 Docker Compose 啟動專案
```bash
docker-compose up --build
```
啟動後，app.py（LINE Bot 服務）與 scheduler.py（定時新聞推播）會同時啟動。
預設會監聽 5001 埠號。








