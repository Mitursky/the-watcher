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
    type = message.text.split(' ')[2]

    if user['tracking'].get(name):
        url = user['tracking'][name]['url']
    else:
        user['tracking'][name] = {"url":url, "name":name}
    # try:
    responce = pager.update(name, url, id, type)
    # except selenium.common.exceptions.InvalidArgumentException:
    #     bot.send_message(id, "Сайт недоступен :(")
    #     return
    
    user['tracking'][name]["update"] = time.time()
    
    db.save(id, {"$set":user})
    
    answer_text = ''
    if responce['status'] == 'update':
        if responce.get('changes_count') and responce['changes_count'] > 0:
            for i in range(responce['changes_count']):
                print(responce['path']+'/changes/'+str(i)+'.png')
                bot.send_photo(id, caption='В этих элементах что-то поменялось', photo=open(responce['path']+'/changes/'+str(i)+'.png', 'rb'))
        else:
            if responce['is_change']:
                answer_text = 'Изменившиеся элементы'
                bot.send_photo(id, caption=answer_text, photo=open(responce['path']+'/difference.png', 'rb'))

                bot.send_photo(id, caption='Обновленная страница', photo=open(responce['path']+'/img.png', 'rb'))
            else:
                answer_text = 'Возможно я конечно туплю, но вроде как на странице ничего не имзенилось'
                bot.send_photo(id, caption=answer_text, photo=open(responce['path']+'/img.png', 'rb') )
           
       
    else:
        answer_text = '😎 Готово, теперь я слежу за этой страницей'
        bot.send_photo(id, caption=answer_text, photo=open(responce['path']+'/img.png', 'rb') )

bot.polling(none_stop=True, interval=0)

