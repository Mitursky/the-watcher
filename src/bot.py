from dataclasses import dataclass
import telebot
from telebot import types
from modules.db.index import *


# tgbot = telebot.TeleBot("5336971557:AAHzRGUHFcHRuv4cehvjisgil2tbYXyQpj0")
tgbot = telebot.TeleBot("5319657728:AAHr-YEuXZjCZyHI7fH6guW_XUuTjam4hC0")


class Bot:

    """
    Create a Bot object.
    :param tgbot: parent Telegram bot.
    :param rules: rules
    """

    def __init__(self, tgbot):
        self.tg = tgbot
        self.rules = []

        @tgbot.message_handler(content_types=["text"])
        def get_text_messages(message):

            """
            Call a function that checks if the received message is the rule.
            :param message: message that was received.
            """

            message.type = "message"
            flag = False
            for i in self.rules:
                if i["text"] in message.text.lower():
                    i["callback"](message, tgbot)
                    flag = True
            if not flag:
                return message.text

        self.get_text_messages = get_text_messages

        @tgbot.callback_query_handler(lambda call: True)
        def get_callback_message(message: types.CallbackQuery):

            """
            Call a function that checks if the received callback is the rule.
            :param callback: callback that was received.
            """

            flag = False
            message.message.text = message.data
            message.message.type = "callback"

            for i in self.rules:
                if i["text"] in message.data.lower():
                    i["callback"](message.message, tgbot)
                    flag = True
            if not flag:
                return message.data

    def new_message(self, text, callback):

        """
        Append new rule to the existent array of rules.
        Rule is a dict with two params - "text" for the message function should receive
        and "callback" for a callback it must do for this text.
        """

        self.rules.append({"text": text, "callback": callback})

    def edit_message_text(message, tgbot,  text):
        if message.caption:
            tgbot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.message_id,
                caption=text,
                reply_markup=None,
            )
        else:
            tgbot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=text,
            )


bot = Bot(tgbot)
