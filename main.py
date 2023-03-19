import time
import sys
import os
from dotenv import load_dotenv
from mastodon_client import MastodonClient
from chat_gpt import ChatGPTClient, create_chat_gpt_client
from database import User, create_session
from background_tasks import (
    get_user_from_db,
    update_user_in_db,
    delete_user_from_db,
    write_log,
    handle_api_error,
    handle_db_error,
    verify_user,
    authenticate_user,
    is_user_ignored,
    add_user_to_ignore_list,
)
from config import get_config
from utils import load_env_vars
from background_tasks import BackgroundTasks
import threading

def main():
    load_env_vars()  # Load .env variables
    config = get_config()  # Get configuration from config.py
    # config.pyからADMIN_USER_IDを取得
    admin_user_id = config.get_admin_user_id()

    # インスタンス作成、設定ファイルの読み込み、ログの設定など
    # MastodonClientインスタンスを作成
    mastodon_client = MastodonClient(
        client_id=config.get_mastodon_client_id(),
        client_secret=config.get_mastodon_client_secret(),
        access_token=config.get_mastodon_access_token(),
        api_base_url=config.get_mastodon_api_base_url(),
    )

    # ChatGPTClientインスタンスを作成
    chat_gpt_client = create_chat_gpt_client(
        api_key=config.get_chat_gpt_api_key(),
        api_base_url=config.get_chat_gpt_api_base_url(),
    )

    # BackgroundTasksインスタンスを作成
    background_tasks = BackgroundTasks()
    background_thread = threading.Thread(target=background_tasks.run)
    background_thread.start()

    while True:
        # ユーザーがフォローされた場合の処理
        new_followers = mastodon_client.get_new_followers()
        for follower in new_followers:
            if not background_tasks.is_user_ignored(follower["id"]):
                mastodon_client.follow_user(follower["id"])

        # ユーザーが無視リストに追加された場合の処理
        ignored_users = background_tasks.get_ignore_list_from_db()
        for user_id in ignored_users:
            if mastodon_client.is_following(user_id):
                mastodon_client.unfollow_user(user_id)

        # メンションの処理
        process_mentions(chat_gpt_client, mastodon_client, config)

        # 一定時間待機
        time.sleep(0.1)  # 100ms

def process_mentions(chat_gpt_client, mastodon_client, config):
    # メンションを取得し、それに対する返信を生成して投稿する処理
    notifications = mastodon_client.get_notifications()

    for notification in notifications:
        if notification["type"] == "mention":
            user_id = notification["account"]["id"]

            if background_tasks.is_user_ignored(user_id):
                continue

            user = get_user_from_db(user_id)
            if not user:
                user = authenticate_user(user_id)

            prompt = notification["status"]["content"]

            if user_id == config.get_admin_user_id():
                if prompt == "\\quit":
                    exit()
                elif prompt == "\\reload":
                    config.reload()
                    mastodon_client = MastodonClient(
                        client_id=config.get_mastodon_client_id(),
                        client_secret=config.get_mastodon_client_secret(),
                        access_token=config.get_mastodon_access_token(),
                        api_base_url=config.get_mastodon_api_base_url(),
                    )
                    chat_gpt_client = create_chat_gpt_client(
                        api_key=config.get_chat_gpt_api_key(),
                        api_base_url=config.get_chat_gpt_api_base_url(),
                    )
                    continue

            response = chat_gpt_client.generate_response(prompt)
            mastodon_client.post_status(response, visibility="direct")

def follow_user(mastodon_client, user_id):
    # ユーザーをフォローする処理
    mastodon_client.follow_user(user_id)
    write_log("info", f"Followed user {user_id}")

def unfollow_user(mastodon_client, user_id):
    # ユーザーのフォローを解除する処理
    mastodon_client.unfollow_user(user_id)
    write_log("info", f"Unfollowed user {user_id}")

if __name__ == "__main__":
    main()
