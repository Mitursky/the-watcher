print("add tracking")
from bot import *


# @tgbot.message_handler(text=["➕ добавить отслеживание"])
# def add_track(message, tgbot):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["⬅ Назад", "➕ Добавить сайт"]
#     markup.add(back_button)
#     tgbot.send_message(
#         message.chat.id,
#         text="С".format(message.from_user),
#         reply_markup=markup,
#     )


def get_new_track(message, tgbot):
    global sites
    sites.append(message.text)
    tgbot.send_message(
        message.from_user.id,
        "Отправьте ссылку на страницу, которую хотите отслеживать: ",
    )
    get_new_track_name(message, tgbot)


def get_new_track_name(message, tgbot):
    global site_nicknames
    if " " in message.text:
        tgbot.send_message(
            message.from_user.id, "Название отслеживание не должно содержать пробелы"
        )
        get_new_track_name(message, tgbot)
    tgbot.send_message(
        message.from_user.id,
        "Назовите своё новое отслеживание (латиницей, без пробелов): ",
    )


@tgbot.message_handler(text=["➕ добавить сайт"])
def prestart_track(bot):
    print("back")
    bot.new_message(text="➕ добавить сайт", callback=get_new_track)
