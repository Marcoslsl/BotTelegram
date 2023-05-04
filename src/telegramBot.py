from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

class TelegramBot:

    def __init__(self) -> None:
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"

    def start(self):

        update_id = None

        while True:
            update = self.get_message(update_id)
            print(update)
            messages = update['result']
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        message_text = message['message']['text']
                        answer_bot = self.create_answer(message_text)

                        self.send_answer(chat_id, answer_bot)
                    except Exception as e:
                        print(e)
                        pass

    def get_message(self, update_id: str) -> any:

        link_request = f"{self.url}getUpdates?timeout=1000"

        if update_id:
            # get the last message
            link_request = f"{self.url}getUpdates?timeout=1000&offset={update_id + 1}"

        results = requests.get(link_request)
        return json.loads(results.content)

    def create_answer(self, message_text):
        if message_text in ["oi", "ola", "eae"]:
            return 'ola, tudo bem?'
        else:
            return 'nao entendi'

    def send_answer(self, chat_id: str, answer: str) -> None:
        link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
        r = requests.get(link_to_send)
        return None