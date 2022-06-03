print("add tracking")
from bot import *


@tgbot.message_handler(text=["➕ добавить отслеживание"])
def get_new_track(message, tgbot):
    tgbot.send_message(
        message.from_user.id,
        'Введите "добавить [ссылка] [название]", чтобы добавить новое отслеживание',
    )


@tgbot.message_handler(text=["➕ добавить отслеживание"])
def prestart_track(bot):
    bot.new_message(text="➕ добавить отслеживание", callback=get_new_track)
    bot.new_message(text="добавить", callback=add_tracking)


@tgbot.message_handler(text=["добавить"])
def add_tracking(message, tgbot):
    track_url = str(message.text).split(" ")[1]
    track_name = str(message.text).split(" ")[2]
    # внесение в базу данных
