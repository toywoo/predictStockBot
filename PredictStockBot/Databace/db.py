import json, psycopg2, os, logging
import pandas as pd
import psycopg2.extras

class DB:
    def __init__(self, logger:logging):
        self.logger = logger
        self.connect = self.connectDB()

    def connectDB(self):
        return _connectDB(self)

    def insertStockNum(self):
        return _insertStockNum(self)
        
    def isStockName(self, target):
        return _isStockName(self, target)

def _connectDB(self):
    print(os.getcwd())
    with open("PredictStockBot\key\db.json", 'r') as f:
            dbInfo = json.load(f)
    try:
        connection = psycopg2.connect(port=dbInfo["port"], host=dbInfo["host"], database=dbInfo["database"], user=dbInfo["user"], password=dbInfo["password"])
    except Exception as e:
        self.logger.info('postgressql database connection error!')
        print(e)
    else:
        self.logger.info('postgressql connect db!')
        return connection

def _insertStockNum(self):
    stockNumDF = pd.read_excel('PredictStockBot\Databace\stock_num_data.xlsx')
    stock_numData = []
    stock_num_ser = stockNumDF["stock_num"]
    stock_name_ser = stockNumDF["stock_name"]
    stock_market_ser = stockNumDF["market"]
    stock_num = stock_num_ser.to_list()
    stock_name = stock_name_ser.to_list()
    stock_market = stock_market_ser.to_list()
    i=0
    while i < stockNumDF.shape[0]:
        stockInfo = []
        stockInfo.append(stock_num[i])
        stockInfo.append(stock_name[i])
        stockInfo.append(stock_market[i])
        stock_numData.append(tuple(stockInfo))
        stockInfo.clear() 
        i = i + 1
    try:
        with self.connectDB() as con:
            with con.cursor() as cur:    
                psycopg2.extras.execute_values(cur, 'INSERT INTO public.stock_num (stock_num, name, market_name) VALUES %s', stock_numData)
    except Exception as e:
        print('insertClass Error: ', e)
    else:
        self.logger.info("adding 'stock_num' data in 'stock_num' table")

def _isStockName(self, target):
    try:
        with self.connectDB() as con:
            with con.cursor() as cur:   
                cur.execute('SELECT stock_num FROM public.stock_num where name = %s or stock_num = %s;', (target, target))
                for stockNum in cur:
                    return stockNum[0]
    except Exception as e:
        self.logger.info('insertClass' + str(e))
        return False