from dotenv import load_dotenv
import requests
import os
import json
from .driveBot import DriveBot
from .visualization.vizualize import *

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

                        self.send_answer(chat_id, answer_bot[0], answer_bot[1] )
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

        bot = DriveBot()
        df = bot.get_data()

        if message_text in ["oi", "ola", "eae", "/start"]:
            return """
                ola, tudo bem?
            1 - NPS interno mensal medio por setor\n
            2 - NPS interno mensal medio por contratacao\n
            3 - Distribuicao do NPS\n
            """, False
        elif message_text == '1':
            return plot_bar_nps(df), True
        elif message_text == '2':
            return plot_bar_cont(df), True
        elif message_text == '3':
            return plot_hist_nps(df), True
        else:
            return 'selecione uma das opcoes acima'

    def send_answer(self, chat_id: str, answer: str, fig_bool: bool) -> None:
        if fig_bool:
            figure = "/home/marcos/Documentos/Projetos/BotTelegram/last_graph.png"
            file = {
                "photo": open(figure, "rb")
            }
            link_to_send = f"{self.url}sendPhoto?chat_id={chat_id}"
            requests.post(link_to_send, files=file)
        else:
            link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
            r = requests.get(link_to_send)
            return None