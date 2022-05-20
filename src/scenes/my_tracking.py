print("my_trackings")
from bot import *


@tgbot.message_handler(text=["📂 мои отслеживания"])
def my_tracks(message, tgbot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("⬅ Назад")
    markup.add(back_button)
    tgbot.send_message(
        message.chat.id,
        text=f"Список отслеживаемых сайтов:".format(message.from_user),
        reply_markup=markup,
    )


def prestart_my_tracks(bot):
    print("help menu")
    bot.new_message(text="📂 мои отслеживания", callback=my_tracks)
