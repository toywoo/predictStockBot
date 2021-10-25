import logging
from bs4 import BeautifulSoup
from fbprophet import Prophet #linux or macos
import pandas as pd
from psycopg2.extras import LoggingConnection
import requests, re, logging


class PredictionModel:
    def __init__(self, logger:logging):
        self.logger = logger

    def scraper(self, stockNum):
        return _scraper(self, stockNum)
    
    def predictStock(self, stockData):
        return _predictStock(self, stockData)

stockInfo={}

def _scraper(self, stockNum):
    pageNum = 1
    while pageNum < 201: #e 차후 기간을 지정하여 연산을 가능하게 할 예정
        url = 'https://finance.naver.com/item/sise_day.naver?code='+ stockNum + '&page='+ str(pageNum)
        with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as response:
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                parser(soup, pageNum)
                pageNum = pageNum + 1
            else : 
                print(response.status_code)
                logging.info('less 200')
                return stockInfo
    self.logger.info('finish scraping stock data of ' + str(stockNum))
    return stockInfo

def parser(originalHTML, pageNum):
    
    if pageNum == 1:
        tableHead = originalHTML.find_all('th')
        for th in tableHead:
            th = str(th)
            th = th[4:]
            th = th[:-5]
            stockInfo.setdefault(th, [])

    tableRow = originalHTML.find_all('span', attrs={"class":"tah"})

    i = 0
    while i<len(tableRow):
        date = re.sub('<.*?>', '', str(tableRow[i])).replace(".", '-')
        stockInfo.get("날짜").append(date)
        i = i + 1

        closingPrice = re.sub('<.*?>', '', str(tableRow[i])).replace(",", '')
        stockInfo.get("종가").append(closingPrice)
        i = i + 1

        priceDifference = re.sub(pattern = r"\\[t,n]", repl="", string=re.sub('<.*?>', '', str(tableRow[i]))).split()[0]
        stockInfo.get("전일비").append(priceDifference)
        i = i + 1

        marketPrice =  re.sub('<.*?>', '', str(tableRow[i])).replace(",", '')
        stockInfo.get("시가").append(marketPrice)
        i = i + 1

        highPrice = re.sub('<.*?>', '', str(tableRow[i])).replace(",", '')
        stockInfo.get("고가").append(highPrice)
        i = i + 1

        lowPrice = re.sub('<.*?>', '', str(tableRow[i])).replace(",", '')
        stockInfo.get("저가").append(lowPrice)
        i = i + 1

        tradingVolume = re.sub('<.*?>', '', str(tableRow[i])).replace(",", '')
        stockInfo.get("거래량").append(tradingVolume)
        i = i + 1

def _predictStock(self, stockData):
    self.logger.info('start predicting stock price')
    stockDF = pd.DataFrame(stockData)

    data_set = {
        'ds':stockDF["날짜"],
        'y':stockDF["종가"]
    }
    data = pd.DataFrame(data_set)

    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=1, freq='D')
    forecast = model.predict(future)
    fig = model.plot(forecast)
    print('\n\n\n', forecast.shape[0], data.shape[0], '\n\n\n')

    forecastPrice = forecast.loc[forecast.shape[0]-1]['trend'] #e 다양한 예측 결과 제공
    self.logger.info('finish predicting stock price')
    return (fig, forecastPrice) 