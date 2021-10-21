from Bot.TelegramBot import Bot
from Bot.command import Command
import json, logging

with open('key.json', 'r') as f:
    jsonData = json.load(f)
    tele_bot_token = jsonData.get("telegram_bot_token")

predictStockBot = Bot('predictStockBot', tele_bot_token)
command = Command(predictStockBot)
command.commandHandler()
predictStockBot.start()
logging.info('predictStockBot start!')