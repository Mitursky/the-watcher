from bot import *


def help(message, tgbot):

    """
    Call a message, that have descriptions for all bot functions.
    """

    tgbot.send_message(
        message.chat.id,
        text=f"Функции бота: \n • Добавить отслеживание — позволяет поставить на отслеживание новый сайт \n • Мои отслеживания — выводит список из существующих отслеживаний с возможностью удалить или просмотреть его".format(
            message.from_user
        ),
    )


def prestart_help(bot):

    """
    Add help function to bot functionality.
    """

    bot.new_message(text="❔ помощь", callback=help)
