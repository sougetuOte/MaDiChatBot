import os
import json
import time
from datetime import datetime
from typing import Optional
import logging
from sqlalchemy.orm import Session
from database import User, create_session
from database import (
    get_user_from_db,
    update_user_in_db,
    delete_user_from_db,
    get_ignore_list_from_db,
    add_user_to_db_ignore_list,
)
from config import config
from mastodon_client import mastodon_client

#BackgroundTasks
RETRY_DELAY = config.get_bot_retry_interval()
MAX_RETRIES = config.get_bot_retry_limit()
API_CHECK_INTERVAL = config.get_bot_api_check_interval()
MAX_RESTARTS = config.get_bot_error_restart_threshold()
RESTART_TIME_LIMIT = config.get_bot_restart_time_limit()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_from_db(user_id: int, session: Session) -> Optional[User]:
    return session.query(User).filter(User.user_id == user_id).one_or_none()

def update_user_in_db(user_id: int, user_data: dict, session: Session):
    user = get_user_from_db(user_id, session)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        session.commit()
    else:
        logger.warning(f"User with ID {user_id} not found in the database.")

def delete_user_from_db(user_id: int, session: Session):
    user = get_user_from_db(user_id, session)
    if user:
        session.delete(user)
        session.commit()
    else:
        logger.warning(f"User with ID {user_id} not found in the database.")

def write_log(log_file_path: str, log_message: str):
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_message + '\n')

def handle_api_error(error):
    logger.error(f"API error occurred: {error}")

def handle_db_error(error):
    logger.error(f"Database error occurred: {error}")

def verify_user(user_data: dict) -> bool:
    # ユーザー情報を検証する処理（例：ユーザー名の長さ、メールアドレスの形式など）
    # 必要に応じて実装を追加
    return True

def authenticate_user(user_data: dict) -> bool:
    # ユーザーを認証する処理（例：パスワードの照合、トークンの検証など）
    # 必要に応じて実装を追加
    return True

def is_user_ignored(user_id: int) -> bool:
    # データベースから無視リストに登録されたユーザーを取得する
    # (例: ignore_list = get_ignore_list_from_db())
    ignore_list = get_ignore_list_from_db()

    # user_idが無視リストに含まれている場合、Trueを返す
    return user_id in ignore_list

def add_user_to_ignore_list(user_id: int):
    # ユーザーIDをデータベースの無視リストに追加する
    # (例: add_user_to_db_ignore_list(user_id))
    add_user_to_db_ignore_list(user_id)


class BackgroundTasks:
    def __init__(self):
        self.api_error_count = 0
        self.restarts = 0
        self.last_restart = datetime.now()

    def run(self):
        while self.restarts < MAX_RESTARTS:
            try:
                self.run_tasks()
                self.api_error_count = 0
            except APIError:
                self.handle_api_error()
            except Exception as e:
                self.handle_unexpected_error(e)

    def run_tasks(self):
        # ここで定期的に実行したいタスクを実行する
        self.check_new_messages()
        pass

    def handle_api_error(self):
        self.api_error_count += 1
        if self.api_error_count >= MAX_RETRIES:
            self.api_error_count = 0
            self.inform_user_of_error()
            self.pause_and_check_api()

    def inform_user_of_error(self):
        # ユーザーにエラーを通知するコード
        send_message_to_user("API エラーが発生しました。機能が一時的に停止します。")
        pass

    def pause_and_check_api(self):
        while True:
            time.sleep(API_CHECK_INTERVAL)
            if self.api_is_responsive():
                break

    def api_is_responsive(self):
        # APIが機能しているか確認するコード
        api_url = config.MASTODON_API_BASE_URL.rstrip('/') + "/status"
        response = requests.get(api_url)
        response = requests.get("https://api.example.com/status")
        return response.status_code == 200
        pass

    def handle_unexpected_error(self, e):
        now = datetime.now()
        if (now - self.last_restart).total_seconds() < RESTART_TIME_LIMIT:
            self.restarts += 1
        else:
            self.restarts = 0
        self.last_restart = now

        if self.restarts >= MAX_RESTARTS:
            self.exit_program()

        time.sleep(RETRY_DELAY)
        self.run()

    def send_message_to_user(user_id: str, message: str):
        mastodon_client.post_status(status=message, visibility="direct", in_reply_to_id=user_id)

    def exit_program(self):
        # プログラムを終了するコード
        send_message_to_user("プログラムが繰り返しエラーを検出しました。プログラムを終了します。")
        sys.exit()
        pass