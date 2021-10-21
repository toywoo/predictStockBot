from numpy import e
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, MessageHandler, CallbackContext, Filters
from telegram.files.inputmedia import InputMedia
import io, logging

from .TelegramBot import Bot
from Databace.db import DB
from Prediction.prediction import PredictionModel

class Command:
    def __init__(self, bot:Bot):
        self.bot = bot
        self.db = DB()
        self.prediction = PredictionModel()

    def commandHandler(self):
        return _commandHandler(self)
    
    def predict(self):
        return _predict(self)

PREDICT = 0
def _commandHandler(self):
    predictHandler = ConversationHandler(
        entry_points=[CommandHandler('predict', getStockName)],
        states={
            PREDICT:[MessageHandler(Filters.text, _predict)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    self.bot.addHandler(predictHandler)

def getStockName(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text= '예측을 원하시는 종목의 이름이나 번호를 입력해주세요!')
    return PREDICT

def _predict(self, update:Update, context:CallbackContext):
    stockName = update.message.text
    stockName = stockName.replace(" ", "")
    logging.info('someone search', stockName)
    stockNum = self.db.isStockName(stockName)
    bot = context.bot
    if stockNum:
        stockInfo = self.prediction.scraper(stockNum) #e 차후 기간을 지정하여 연산을 가능하게 할 예정
        forecastData = self.prediction.predictStock(stockInfo)
        logging.info('someone success forecasting', stockNum)
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat.id
        bio = io.BytesIO()
        forecastData[0].savefig(bio, format='png')
        bio.seek(0)
        bot.send_photo(chat_id=chat_id, photo=bio)
        bot.send_message(chat_id, text=forecastData[1])
        logging.info('someone received forecasted Data of', stockNum)
    else:
        logging.info('fail! search stock number.')
        bot.send_message('입력하신 종목 이름이나 번호가 맞는지 확인해주세요. (혹시 6자리가 맞나요? 종목의 이름이 정식 등록된 명칭인가요? e.g. YG -> 와이지엔터테인먼트')
    return ConversationHandler.END

def cancel(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text = '작업이 모두 취소 되었습니다.')
    return ConversationHandler.entry_points