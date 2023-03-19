import os
from dotenv import load_dotenv

class ConfigIO:
    def __init__(self):
        load_dotenv()
        # Mastodon Settings
        self.MASTODON_API_BASE_URL = os.getenv('MASTODON_API_BASE_URL')
        self.MASTODON_CLIENT_SECRET = os.getenv('MASTODON_CLIENT_SECRET')
        self.MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')
        self.MASTODON_BOT_ACCOUNT_ID = os.getenv('MASTODON_BOT_ACCOUNT_ID')

        # Administrator
        self.ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')

        # ChatGPT API
        self.CHAT_GPT_API_KEY = os.getenv('CHAT_GPT_API_KEY')
        self.CHAT_GPT_MODEL_VERSION = int(os.getenv('CHAT_GPT_MODEL_VERSION'))
        self.CHAT_GPT_SPEED_PRIORITY = os.getenv('CHAT_GPT_SPEED_PRIORITY') == 'True'

        # Database Settings
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_PORT = int(os.getenv('DB_PORT'))

        # Bot Settings
        self.BOT_NAME = os.getenv('BOT_NAME')
        self.BOT_GENDER = os.getenv('BOT_GENDER')
        self.BOT_AGE = int(os.getenv('BOT_AGE'))
        self.BOT_JOB = os.getenv('BOT_JOB')
        self.BOT_APPEARANCE = os.getenv('BOT_APPEARANCE')

        # Catchphrases
        self.BOT_CATCHPHRASES = os.getenv('BOT_CATCHPHRASES').split('|')

        # Conversation Settings
        self.MAX_ACTIVE_USERS = int(os.getenv('MAX_ACTIVE_USERS'))
        self.MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH'))
        self.MAX_OUTPUT_LENGTH = int(os.getenv('MAX_OUTPUT_LENGTH'))
        self.MAX_CHATGPT_TOKENS = int(os.getenv('MAX_CHATGPT_TOKENS'))
        self.USER_TIMEOUT = int(os.getenv('USER_TIMEOUT'))
        self.MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH'))
        self.APOLOGY_MESSAGE = os.getenv('APOLOGY_MESSAGE')
        self.BOT_RETRY_INTERVAL = int(os.getenv('BOT_RETRY_INTERVAL'))
        self.BOT_RETRY_LIMIT = int(os.getenv('BOT_RETRY_LIMIT'))
        self.BOT_ERROR_RESTART_THRESHOLD = int(os.getenv('BOT_ERROR_RESTART_THRESHOLD'))
        self.BOT_API_CHECK_INTERVAL = int(os.getenv('BOT_API_CHECK_INTERVAL'))
        self.BOT_RESTART_TIME_LIMIT = int(os.getenv('BOT_RESTART_TIME_LIMIT'))

    #.envのリロード
    def reload(self):
        load_dotenv()

    # Getter methods
    def get_database_uri(self):
        return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_mastodon_api_base_url(self):
        return self.MASTODON_API_BASE_URL

    def get_mastodon_client_secret(self):
        return self.MASTODON_CLIENT_SECRET

    def get_mastodon_access_token(self):
        return self.MASTODON_ACCESS_TOKEN

    def get_mastodon_bot_account_id(self):
        return self.MASTODON_BOT_ACCOUNT_ID

    def get_admin_user_id(self):
        return self.ADMIN_USER_ID

    def get_chat_gpt_api_key(self):
        return self.CHAT_GPT_API_KEY

    def get_chat_gpt_model_version(self):
        return self.CHAT_GPT_MODEL_VERSION

    def get_chat_gpt_speed_priority(self):
        return self.CHAT_GPT_SPEED_PRIORITY

    def get_database_uri(self):
        return self.database_uri

    def get_bot_name(self):
        return self.BOT_NAME

    def get_bot_gender(self):
        return self.BOT_GENDER

    def get_bot_age(self):
        return self.BOT_AGE

    def get_bot_job(self):
        return self.BOT_JOB

    def get_bot_appearance(self):
        return self.BOT_APPEARANCE

    def get_bot_catchphrases(self):
        return self.BOT_CATCHPHRASES

    def get_max_active_users(self):
        return self.MAX_ACTIVE_USERS

    def get_max_input_length(self):
        return self.MAX_INPUT_LENGTH

    def get_max_output_length(self):
        return self.MAX_OUTPUT_LENGTH

    def get_max_chatgpt_tokens(self):
        return self.MAX_CHATGPT_TOKENS

    def get_user_timeout(self):
        return self.USER_TIMEOUT

    def get_max_message_length(self):
        return self.MAX_MESSAGE_LENGTH

    def get_apology_message(self):
        return self.APOLOGY_MESSAGE

    def get_bot_retry_interval(self):
        return self.BOT_RETRY_INTERVAL

    def get_bot_retry_limit(self):
        return self.BOT_RETRY_LIMIT

    def get_bot_error_restart_threshold(self):
        return self.BOT_ERROR_RESTART_THRESHOLD

    def get_bot_api_check_interval(self):
        return self.BOT_API_CHECK_INTERVAL

    def get_bot_restart_time_limit(self):
        return self.BOT_RESTART_TIME_LIMIT

    # Setter methods

    # Mastodon Settings
    # Administrator
    # ChatGPT API
    # Database Settings
    # Bot Settings
    # これらの情報は現在プログラムからの編集は不可とする

    # Conversation Settings
    def set_max_active_users(self, max_users):
        # max_usersが整数であることを確認
        if isinstance(max_users, int):
            self._MAX_ACTIVE_USERS = max_users
        else:
            raise ValueError("Max active users must be an integer.")

config = ConfigIO()
