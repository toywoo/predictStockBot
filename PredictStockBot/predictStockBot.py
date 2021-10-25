from Bot.TelegramBot import Bot
from Bot.command import Command
import json, logging

with open('PredictStockBot\key\key.json', 'r') as f:
    jsonData = json.load(f)
    tele_bot_token = jsonData.get("telegram_bot_token")

predictStockBot = Bot('predictStockBot', tele_bot_token)
logger = predictStockBot.makeLogger('Predict_Stock_Bot')
command = Command(predictStockBot, logger)
command.commandHandler()
predictStockBot.start()
logger.info('predictStockBot start!')


#it can run in anaconda kernel