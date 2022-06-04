from bot import *


def menu(message, tgbot):

    """
    Calls the menu of the bot.

    :param markup: the markup for reply keyboard buttons.
    :param buttons: the array of main functionality buttons.
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # array for all the buttons options
    buttons = ["➕ Добавить отслеживание", "📂 Мои отслеживания", "❔ Помощь"]

    # loop for adding all the buttons to markup
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

    """
    Add menu function to bot functionality, which will be first started when the command /start is written.
    """

    bot.new_message(text="/start", callback=menu)
