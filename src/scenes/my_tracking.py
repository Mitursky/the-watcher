print("my_trackings")
from bot import *

test_data = [{"name": "google", "url": "google.com"}, {"name": "yan", "url": "ya.ru"}]


@tgbot.message_handler(text=["📂 мои отслеживания"])
def show_tracks(message, tgbot):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(test_data)):
        keyboard.add(
            types.InlineKeyboardButton(
                text=(f"{str(i + 1)}. {test_data[i]['name']}"),
                callback_data="check_track",
            )
        )
    try:
        message = message.message
        tgbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Список отслеживаемых сайтов:",
            reply_markup=keyboard,
        )
    except:
        print("its not callback")
        tgbot.send_message(
            message.chat.id,
            text="Список отслеживаемых сайтов:",
            reply_markup=keyboard,
        )


@tgbot.message_handler(commands=["📂 мои отслеживания"])
def prestart_show_tracks(bot):
    print("help menu")
    bot.new_message(text="📂 мои отслеживания", callback=show_tracks)
    bot.new_message(text="check_track", callback=check_track)
    bot.new_message(text="show_tracks", callback=show_tracks)


def check_track(callback, tgbot):
    print("checking is working")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Проверить элементы", callback_data="check_elements"
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text="Проверить изображения", callback_data="check_images"
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_tracking")
    )
    keyboard.add(
        types.InlineKeyboardButton(text="⬅ Назад", callback_data="show_tracks")
    )
    tgbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(f"Что вы хотите сделать?"),
        reply_markup=keyboard,
    )
