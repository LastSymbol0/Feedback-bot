import datetime
import logging
import telebot
import config

logging.basicConfig(filename="tlg_bot_logs.txt", level=logging.INFO)
logging.info("\n\t\tStart logging\t\t\n\t%s\n~ ~ ~\n" % datetime.datetime.now())
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help', 'echo', 'stop'])
def reply_cmnd(message):
    if (message.text == "/start") | (message.text == "/help"):
        bot.send_message(message.chat.id, config.start_message)
        logging.info("Start bot from user: '%d'\n\t\t%s\n~ ~ ~\n" %
                     (message.chat.id, datetime.datetime.now()))
    if message.text == "/help":
        bot.send_message(message.chat.id, "Commands list:\n/start\n/help\n/echo\n/stop")
    elif message.text == "/echo":
        bot.send_message(message.chat.id, "your echo")


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio"])
def resnd(message):
    if bot.forward_message(config.my_id, message.chat.id, message.message_id):
        bot.reply_to(message, "Спасибо, ваше сообщение доставленно)")
        logging.info("New non-text message from user: '%d' \n\t\t%s\n~ ~ ~\n" %
                     (message.chat.id, datetime.datetime.now()))


@bot.message_handler(content_types=["text"])
def resend(message):
    if message.chat.id == config.my_id:
        reply(message)
    elif bot.forward_message(config.my_id, message.chat.id, message.message_id):
        bot.reply_to(message, "Спасибо, ваше сообщение доставленно)")
        logging.info("New message from user: '%d' with text :'%s'\n\t\t%s\n~ ~ ~\n" %
                     (message.chat.id, message.text, datetime.datetime.now()))


def reply(message):
        if hasattr(message.reply_to_message, 'forward_from'):
            bot.send_message(message.reply_to_message.forward_from.id, message.text)
            logging.info("New reply for user: '%d', message: '%s'\nReply text: '%s'\n\\t\t%s\n~ ~ ~\n" %
                         (message.reply_to_message.chat.id, message.reply_to_message.text, message.text, datetime.datetime.now()))
        else:
            bot.send_message(config.my_id, "reply, plz")


bot.polling(none_stop=True, interval=0.4)
