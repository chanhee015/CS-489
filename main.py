import sys
import bot_skeleton

# def proc_stop(bot, update):
#     cs489.sendMessage('End of test.')
#     cs489.stop()

def ethics_test(bot, update):
    cs489.sendMessage('Starting Ethics test')
    test_function()

def test_function()


cs489 = bot_skeleton.Ethicsbot()
cs489.add_handler('test', ethics_test)
cs489.start()