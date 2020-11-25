import telegram
import telepot
from telegram.ext import Updater, CommandHandler

class TelegramBot:  
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = 1334060345
        self.name = name

    def sendMessage(self, text, user_id):
        self.core.sendMessage(chat_id = user_id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

class Ethicsbot(TelegramBot):
    def __init__(self):
        self.token = '1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs'
        TelegramBot.__init__(self, ' ', self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def start(self, user_id):
        self.sendMessage('Start of test.', user_id)  
        msg = "User's id: " + str(self.id)
        self.sendMessage(msg, user_id)
        self.updater.start_polling()
        self.updater.idle()