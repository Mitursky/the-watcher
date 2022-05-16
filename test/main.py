import telebot
bot = telebot.TeleBot('5319657728:AAHr-YEuXZjCZyHI7fH6guW_XUuTjam4hC0')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет")

bot.polling(none_stop=True, interval=0)