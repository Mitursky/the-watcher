import telebot
from telebot import types

print("bot")
tgbot = telebot.TeleBot("5336971557:AAHzRGUHFcHRuv4cehvjisgil2tbYXyQpj0")


class Bot:
    def __init__(self, tgbot):
        self.tg = tgbot
        self.rules = []

        @tgbot.message_handler(content_types=["text"])
        def get_text_messages(message):
            print(message.text.lower())
            for i in self.rules:
                if i["text"] in message.text.lower():
                    i["callback"](message, tgbot)

    def new_message(self, text, callback):
        self.rules.append({"text": text, "callback": callback})


bot = Bot(tgbot)
