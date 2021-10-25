from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, MessageHandler, CallbackContext, Filters
import io, logging

from .TelegramBot import Bot
from Databace.db import DB
from Prediction.prediction import PredictionModel

class Command:
    def __init__(self, bot:Bot, logger:logging):
        self.bot = bot
        self.logger = logger
        self.db = DB(self.logger)
        self.prediction = PredictionModel(self.logger)

    def commandHandler(self):
        return _commandHandler(self)
    
    def predict(self, update:Update, context:CallbackContext):
        stockName = update.message.text
        stockName = stockName.replace(" ", "")
        self.logger.info('someone search ' + stockName)
        stockNum = self.db.isStockName(stockName)
        bot = context.bot
        if stockNum:
            stockInfo = self.prediction.scraper(stockNum) #e 차후 기간을 지정하여 연산을 가능하게 할 예정
            forecastData = self.prediction.predictStock(stockInfo)
            
            self.logger.info('someone success forecasting '+ stockNum)
            chat_id = update.message.chat.id
            bio = io.BytesIO()
            forecastData[0].savefig(bio, format='png')
            bio.seek(0)
            bot.send_photo(chat_id=chat_id, photo=bio)
            bot.send_message(chat_id, text=forecastData[1])
            self.logger.info('someone received forecasted Data of ' + stockNum)
        else:
            chat_id = update.message.chat_id
            self.logger.info('fail! search stock number.')
            bot.send_message(chat_id=chat_id, text='입력하신 종목 이름이나 번호가 맞는지 확인해주세요. (혹시 6자리가 맞나요? 종목의 이름이 정식 등록된 명칭인가요? e.g. YG -> 와이지엔터테인먼트')
        return ConversationHandler.END

PREDICT = 0
def _commandHandler(self):
    predictHandler = ConversationHandler(
        entry_points=[CommandHandler('predict', getStockName)],
        states={
            PREDICT:[MessageHandler(Filters.text, self.predict)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    self.bot.addHandler(predictHandler)

def getStockName(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = update.message.chat_id
    bot = context.bot
    bot.send_message(chat_id, text="예측을 원하시는 종목의 이름이나 번호를 입력해주세요!")
    return PREDICT



def cancel(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text = '작업이 모두 취소 되었습니다.')
    return ConversationHandler.entry_points