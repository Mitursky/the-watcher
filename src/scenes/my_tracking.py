
from bot import *
import datetime
from modules.db.index import *
from modules.pager.index import *
test_data = [{"name": "google", "url": "google.com"}, {"name": "yan", "url": "ya.ru"}]

def generate_checking_msg(current_track):
    # convert current_track['update'] in time.time() format to date format as day.month.year hour:minute:second
    converted_time = datetime.datetime.fromtimestamp(
        current_track['update']
    ).strftime("%d.%m.%Y %H:%M:%S")

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Проверить элементы", callback_data="check_elements/" + current_track['name']
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text="Проверить изображения", callback_data="check_images/"+ current_track['name']
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_track/" + current_track['name'])
    )
    keyboard.add(
        types.InlineKeyboardButton(text="⬅ Назад", callback_data="show_tracks")
    )
    return keyboard, f"Отслеживаемый сайт: {current_track['name']}\nСсылка: {current_track['url']}\nПоследнее обновление: {converted_time}"

def show_tracks(message, tgbot):
    """
    Call function with inline keyboard with all the existent trackings of user.
    :param keyboard: keyboard with all trackings.
    :param user: id of current user.
    """
    user = db.find(message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    num = 0
    for i in user["tracking"]:
        num += 1
        keyboard.add(
            types.InlineKeyboardButton(
                text=(f"{str(num)}. {user['tracking'][i]['name']}"),
                callback_data="check_track/" + user['tracking'][i]['name'],
            )
        )

    # if len of user["tracking"] == 0: send message with text "У вас нет активных отслеживаний"
    if len(user["tracking"]) == 0:
        tgbot.send_message(message.chat.id, "У вас нет активных отслеживаний")
        return

    if message.type == "callback":
        # if messages includes caption send new message wihout caption
        if message.caption:
            tgbot.send_message(message.chat.id, "Список отслеживаемых сайтов:", reply_markup=keyboard)
        else:
            tgbot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text="Список отслеживаемых сайтов:",
                reply_markup=keyboard,
            )
    else:
        tgbot.send_message(
            message.chat.id,
            text="Список отслеживаемых сайтов:",
            reply_markup=keyboard,
        )

def prestart_show_tracks(bot):
    bot.new_message(text="📂 мои отслеживания", callback=show_tracks)
    bot.new_message(text="check_track", callback=check_track)
    bot.new_message(text="check_images", callback=check_images)
    bot.new_message(text="show_tracks", callback=show_tracks)
    bot.new_message(text="delete_track", callback=delete_track)

# def ho remove the tracking
def delete_track(message, tgbot):
    user = db.find(message.chat.id)

    # make keyboard width button Назад
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="⬅ Назад", callback_data="show_tracks")
    )
    # delete current_track from user's tracking object
    del user['tracking'][message.text.split('/')[1]]
    remove_text = '❌ Отслеживание удалено'

    if message.caption:
        tgbot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.message_id,
            caption=remove_text,
            reply_markup=keyboard,
        )
    else:
        tgbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=remove_text,
            reply_markup=keyboard,
        )

    db.save(
            message.chat.id,
           {"$set":user},
        )

# def check_images ho call pager.update and check the images
def check_images(message, tgbot):
    """
    Call function that will check if the image of site have been changed.
    :param current_track: current track that user's chosen.
    :param user: id of current user.
    :param response: an object that has an information about if image's changed and how has it been changed.
    :param answer_text: text that will be displayed according on if there is a change or no change. Have 2 varieties of displaying.
    :param answer_photo:
    """

    # if message contatin caption, edit caption else edit message
    if message.caption:
        tgbot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.message_id,
            caption=f"⌚ Сравниваем изменения в изображении {message.text.split('/')[1]}, это может занять от одной секунды до нескольких минут.",
            reply_markup=None,
        )
    else:
        tgbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"⌚ Сравниваем изменения в изображении {message.text.split('/')[1]}, это может занять от одной секунды до нескольких минут.",
        )

    user = db.find(message.chat.id)
    current_track = user['tracking'][message.text.split('/')[1]]

    # call pager.update and check the images
    response = pager.update(id=message.chat.id, name=current_track['name'], url=current_track['url'], type="img", message=message, tgbot=tgbot)
    answer_text = ''
    answer_photo = ''
    if response['is_change']:
        answer_text = '🔎 Обнаружены изменения. Изменившиеся области отражены на изображении.'
        answer_photo = response['path']+'/difference.png'
    else:
        answer_text = '✅ Изменений не обнаружено.'
        answer_photo = response['path']+'/img.png'

    # set the new update time
    current_track['update_time'] = time.time()
    user['tracking'][message.text.split('/')[1]] = current_track
    db.save(message.chat.id, {"$set":user})

    keyboard, text  = generate_checking_msg(current_track)
    tgbot.delete_message(message.chat.id, message.message_id)

    # send answer_photo width answer_text and keyboard
    tgbot.send_photo(message.chat.id, caption=answer_text+'\n\n'+text, photo=open(answer_photo, 'rb'), reply_markup=keyboard)

   

def check_track(message, tgbot, answer=None):
    """
    Call function that will show buttons of interaction with chosen tracking. 
    :param current_track: current track that user's chosen.
    :param user: id of current user.
    :param keyboard: inline buttons list. 
    """
    user = db.find(message.chat.id)
    current_track = user['tracking'][message.text.split('/')[1]]

    
    # send message with current_track name, url and update time
    keyboard, text = generate_checking_msg(current_track)

    tgbot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
    )

