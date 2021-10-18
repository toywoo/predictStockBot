import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from fbprophet import Prophet #linux or apple

stockNum = '086790'
pageNum = '1'
url = 'https://finance.naver.com/item/sise_day.naver?code='+ stockNum + '&page='+ pageNum

with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as response:
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

    else : 
        print(response.status_code)


stockInfo={}

tableHead = soup.find_all('th')

for th in tableHead:
    th = str(th)
    th = th[4:]
    th = th[:-5]
    stockInfo.setdefault(th, [])

tableRow = soup.find_all('span', attrs={"class":"tah"})

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

stockDF = pd.DataFrame(stockInfo)

data_set = {
    'ds':stockDF["날짜"],
    'y':stockDF["종가"]
}
data = pd.DataFrame(data_set)

model = Prophet()
model.fit(data)
future = model.make_future_dataframe(periods=1, freq='D')
forecast = model.predict(future)
fig1 = model.plot(forecast)
forecast.loc[2002]