from bot import *
import re
from modules.db.index import *
from modules.pager.index import *
import playwright


def get_new_track(message, tgbot):

    """
    Call message with explanation of how to add tracking.
    """

    tgbot.send_message(
        message.from_user.id,
        f'Введите "добавить [ссылка] [название]", чтобы добавить новое отслеживание.\nНапример: "добавить https://www.google.com Гугл"',
    )


def prestart_track(bot):

    """
    Add functions of add tracking (get_new_track and add_tracking) to bot functionality.
    """

    bot.new_message(text="➕ добавить отслеживание", callback=get_new_track)
    bot.new_message(text="добавить", callback=add_tracking)


def add_tracking(message, tgbot):

    """
    Add new tracking in DB, using split to get url and name from the message.
    :param track_url: url of the tracking.
    :param track_name: name of the tracking.
    """

    # if first word in message is not "добавить" return
    if message.text.split()[0] != "добавить":
        return

    user = db.find(message.from_user.id)

    # if user tracking list >= 10, send message to user and return
    if len(user["tracking"]) >= 10:
        tgbot.send_message(
            message.from_user.id,
            f"У вас уже есть 10 отслеживаний. Удалите одно из них, чтобы добавить новое.",
        )
        return

    track_url = str(message.text).split(" ")[1]
    track_name = str(message.text).split(" ")[2]

    # delete all symbols in track name except letters and numbers on rus or eng
    track_name = re.sub(r"[^a-zA-Z0-9а-яА-Я]", "", track_name)

    # make track_url as url
    track_url = re.sub(r"^https?:\/\/", "", track_url)
    track_url = re.sub(r"\/$", "", track_url)
    track_url = "https://" + track_url

    if user["tracking"].get(track_name):
        # send message about track name are used and return
        tgbot.send_message(
            message.chat.id,
            f'У вас уже есть отслеживание с названием "{track_name}". Выберите другое название.',
        )
        return
    else:
        # send message about track added
        tgbot.send_message(
            message.chat.id,
            f'⌚ Добавляем "{track_name}", это может занять от одной секунды до нескольких минут.',
        )
        try:
            response = pager.update(track_name, track_url, message.from_user.id, "img")
        except playwright._impl._api_types.Error:
            # send message about error
            tgbot.send_message(
                message.chat.id,
                f"❌ Сайт {track_url} недоступен. Проверьте правильность введенных данных.",
            )
            return
        print(response)

        # add new tracking in DB
        user["tracking"][track_name] = {
            "url": track_url,
            "name": track_name,
            "update": time.time(),
        }
        db.save(
            message.from_user.id,
            {"$set": user},
        )
        tgbot.send_photo(
            message.chat.id,
            caption="😎 Готово, теперь я слежу за этой страницей",
            photo=open(response["path"] + "/img.png", "rb"),
        )
