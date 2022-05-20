from urllib import response
import telebot
from src.modules.pager.pager import *
from src.modules.db.index import *
import time
bot = telebot.TeleBot('5319657728:AAHr-YEuXZjCZyHI7fH6guW_XUuTjam4hC0')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    id = message.from_user.id
    
    user = db.find(id)
    bot.send_message(id, "Привет, делаю для тебя снимок жопы")
    name = message.text.split(' ')[1]
    url = message.text.split(' ')[0]
    
    if user['tracking'].get(name):
        url = user['tracking'][name]['url']
    else:
        user['tracking'][name] = {"url":url, "name":name}
    
    responce = pager.update(name, url, id)
    user['tracking'][name]["update"] = time.time()
    
    db.save(id, {"$set":user})
    
    answer_text = ''
    if responce['status'] == 'update':
       if responce['is_change']:
           answer_text = 'Вот это прикол, кажется на странице что-то изменилось'
       else:
           answer_text = 'Возможно я конечно туплю, но вроде как на странице ничего не имзенилось'
    else:
        answer_text = '😎 Готово, теперь я слежу за этой страницей'
        
    bot.send_photo(id, caption=answer_text, photo=open(responce['path'], 'rb') )

bot.polling(none_stop=True, interval=0)

