print("help")
from bot import *


@tgbot.message_handler(text=["❔ помощь"])
def help(message, tgbot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("⬅ Назад")
    markup.add(back_button)
    tgbot.send_message(
        message.chat.id,
        text=f"Функции бота: \n • Добавить отслеживание — позволяет поставить на отслеживание новый сайт \n • Мои отслеживания — выводит список из существующих отслеживаний с возможностью удалить или просмотреть его".format(
            message.from_user
        ),
        reply_markup=markup,
    )


def prestart_help(bot):
    print("help menu")
    bot.new_message(text="❔ помощь", callback=help)
