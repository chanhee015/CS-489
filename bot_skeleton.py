import telegram
from telegram.ext import Updater, CommandHandler

class TelegramBot:  
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = 1476179514
        self.name = name

    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text)

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

    def start(self):
        self.sendMessage('Start of test.')
        self.sendMessage('go to https://api.telegram.org/bot1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs/getUpdates for log')
        self.updater.start_polling()
        self.updater.idle()