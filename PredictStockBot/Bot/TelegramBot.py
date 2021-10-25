import telegram, logging
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

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def makeLogger(self, name=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

        return logger