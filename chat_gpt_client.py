import openai
import re
from utils import preprocess_gpt_response
import logger

class ChatGPTClient:
    def __init__(
        self,
        api_key: str,
        api_endpoint: str,
        bot_name: str,
        bot_gender: str,
        bot_age: int,
        bot_occupation: str,
        bot_appearance: str,
        bot_catchphrase: str,
    ):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.bot_name = bot_name
        self.bot_gender = bot_gender
        self.bot_age = bot_age
        self.bot_occupation = bot_occupation
        self.bot_appearance = bot_appearance
        self.bot_catchphrase = bot_catchphrase

        openai.api_key = self.api_key

    def generate_response(self, prompt: str, max_tokens: int = 150) -> str:
        # Check if the input contains an image
        if re.search(r"\[image\]", prompt):
            return "画像は解釈できません"

        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{self.bot_name}は{self.bot_gender}で{self.bot_age}歳の{self.bot_occupation}です。{self.bot_appearance}で、キャッチフレーズは「{self.bot_catchphrase}」です。質問者: {prompt}",
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )

        message = completions.choices[0].text.strip()
        processed_message = preprocess_gpt_response(message)
        logger.info(f"Generated response: {processed_message}")
        return processed_message

def create_chat_gpt_client(
    api_key: str,
    api_endpoint: str,
    bot_name: str,
    bot_gender: str,
    bot_age: int,
    bot_occupation: str,
    bot_appearance: str,
    bot_catchphrase: str,
) -> ChatGPTClient:
    return ChatGPTClient(
        api_key,
        api_endpoint,
        bot_name,
        bot_gender,
        bot_age,
        bot_occupation,
        bot_appearance,
        bot_catchphrase,
    )
