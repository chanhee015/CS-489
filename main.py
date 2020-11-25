import sys
import bot_skeleton
import telepot

def ethics_test(bot, update):
    cs489.sendMessage('Starting Ethics test')
    test_function()

token = '1452014249:AAF8xlpe6r3sAq0c3ZJ--HH6I5qT5ZBftQs'
TelegramBot = telepot.Bot(token)
user_id = TelegramBot.getUpdates()[0]["message"]["from"]["id"]
cs489 = bot_skeleton.Ethicsbot()
cs489.add_handler('test', ethics_test)
cs489.start(user_id)