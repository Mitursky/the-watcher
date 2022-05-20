print("main")
from bot import *


@tgbot.message_handler(commands=["start"])
def menu(message, tgbot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_button = types.KeyboardButton("➕ Добавить отслеживание")
    exist_button = types.KeyboardButton("📂 Мои отслеживания")
    help_button = types.KeyboardButton("❔ Помощь")
    markup.add(add_button, exist_button, help_button)
    tgbot.send_message(
        message.chat.id,
        text="Добро пожаловать в наблюдатель, {0.first_name}! Выберите опцию, воспользовавшись кнопками снизу:".format(
            message.from_user
        ),
        reply_markup=markup,
    )


def prestart_menu(bot):
    print("pre2")
    bot.new_message(text="/start", callback=menu)
