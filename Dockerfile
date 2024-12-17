# 使用官方 Python 3.11 基底映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝相依套件
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案到容器中
COPY . /app

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 啟動應用程式
CMD ["python", "app/app.py"]
