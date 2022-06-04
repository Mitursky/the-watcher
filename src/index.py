from bot import *
from scenes.menu import *
from scenes.help import *
from scenes.add_tracking import *
from scenes.my_tracking import *

print('Bot started')

prestart_menu(bot)
prestart_help(bot)
prestart_track(bot)
prestart_show_tracks(bot)


bot.tg.polling(none_stop=True, interval=0)
