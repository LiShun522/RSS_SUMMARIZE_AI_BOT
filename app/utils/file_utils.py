import os
import json
import logging

# 日誌配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def load_data(file_path, default):
    """
    載入 JSON 資料，若檔案不存在則初始化。
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(list(default), f)
        logging.info(f"檔案 {file_path} 不存在，已創建並初始化。")
    try:
        with open(file_path, 'r') as f:
            return set(json.load(f))
    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"讀取檔案 {file_path} 失敗: {e}，重新初始化。")
        return default

def save_data(data, file_path):
    """
    儲存資料至 JSON 檔案。
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(list(data), f)
        logging.info(f"成功保存檔案: {file_path}")
    except Exception as e:
        logging.error(f"保存檔案失敗: {e}")
