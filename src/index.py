from bot import *
from scenes.menu import *
from scenes.help import *


prestart_menu(bot)

bot.tg.polling(none_stop=True, interval=0)
