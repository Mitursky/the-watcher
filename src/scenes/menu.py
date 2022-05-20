print("main")
from bot import *


@tgbot.message_handler(commands=["/start"])
def menu(message, tgbot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["➕ Добавить отслеживание", "📂 Мои отслеживания", "❔ Помощь"]
    for i in buttons:
        markup.add(i)
    tgbot.send_message(
        message.chat.id,
        text="Добро пожаловать в наблюдатель, {0.first_name}! Выберите опцию, воспользовавшись кнопками снизу:".format(
            message.from_user
        ),
        reply_markup=markup,
    )


def prestart_menu(bot):
    print("main menu")
    bot.new_message(text="/start", callback=menu)


@tgbot.message_handler(commands=["⬅ назад"])
def prestart_back(bot):
    print("back")
    bot.new_message(text="⬅ назад", callback=menu)
