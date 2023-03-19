import re
from mastodon import Mastodon
from utils import sanitize_status
import logger

class MastodonClient:
    def __init__(self, api_key: str, instance_url: str):
        self.api_key = api_key
        self.instance_url = instance_url
        self.mastodon = Mastodon(
            access_token=self.api_key,
            api_base_url=self.instance_url
        )

    def post_status(self, status: str, visibility: str = "public") -> str:
        sanitized_status = sanitize_status(status)
        return self.mastodon.status_post(sanitized_status, visibility=visibility)

    def get_notifications(self):
        notifications = self.mastodon.notifications()
        # Decide if you want to log notifications here
        return notifications

    def get_conversation(self, status_id: int):
        return self.mastodon.status_context(status_id)

    def follow_user(self, account_id: int):
        self.mastodon.account_follow(account_id)
        logger.info(f"Followed user with account_id: {account_id}")

    def unfollow_user(self, account_id: int):
        self.mastodon.account_unfollow(account_id)
        logger.info(f"Unfollowed user with account_id: {account_id}")
