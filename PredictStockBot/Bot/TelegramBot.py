import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

class Bot:
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.name = name
    
    def sendMessage(self, chat_id, text, reply_markup=''):
        self.core.sendMessage(chat_id, text=text, reply_markup=reply_markup)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

    def addCommandHandler(self, func, cmd=''):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))
    
    def addHandler(self, handler):
        self.updater.dispatcher.add_handler(handler)

    def start(self, update:Update, context:CallbackContext):
        chat_id = update.callback_query.message.chat.id
        self.sendMessage(chat_id ,'반갑습니다. 당신의 주가 예측기 입니다.') ##c id 변경
        self.updater.start_polling()
        self.updater.idle()