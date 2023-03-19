import os
import re
from datetime import datetime
from typing import List

def sanitize_input(input_str: str) -> str:
    # 不正な文字やコードを除去する処理を実装します。
    sanitized_str = re.sub(r'[^\w\s]', '', input_str)
    return sanitized_str

def sanitize_status(status: str) -> str:
    status = re.sub('<[^<]+?>', '', status)  # Remove HTML tags
    status = re.sub('\n', ' ', status)  # Replace newlines with spaces
    return status.strip()

def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text: str, max_length: int) -> str:
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def preprocess_gpt_response(response: str) -> str:
    # Preprocess GPT response here if necessary
    return response.strip()

def create_error_message(error_code: str) -> str:
    error_messages = {
        'E001': '入力が無効です。',
        'E002': 'データベースエラーが発生しました。',
        'E003': 'システムエラーが発生しました。'
    }
    return error_messages.get(error_code, '不明なエラーが発生しました。')

def ensure_directory_exists(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def write_file(file_path: str, content: str) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_messages_from_history(history: List[str]) -> List[str]:
    return history[::2]

def get_replies_from_history(history: List[str]) -> List[str]:
    return history[1::2]

def summarize_conversation(history: List[str], max_length: int = 100) -> str:
    messages = get_messages_from_history(history)
    replies = get_replies_from_history(history)
    summary = "User: " + " Bot: ".join(messages) + " Bot: " + " User: ".join(replies)
    return truncate_text(summary, max_length)
