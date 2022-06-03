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
            print(message.text)
            flag = False
            for i in self.rules:
                if i["text"] in message.text.lower():
                    i["callback"](message, tgbot)
                    flag = True
            if not flag:
                return message.text

        self.get_text_messages = get_text_messages

        @tgbot.callback_query_handler(lambda call: True)
        def get_callback_message(call: types.CallbackQuery):
            flag = False
            for i in self.rules:
                if i["text"] in call.data.lower():
                    i["callback"](call, tgbot)
                    flag = True
            if not flag:
                return call.data

    def new_message(self, text, callback):
        self.rules.append({"text": text, "callback": callback})


bot = Bot(tgbot)
