CREATE DATABASE predict_stock

CREATE TABLE public.stock_num
(
    stock_num_key SERIAL PRIMARY KEY,
    stock_num VARCHAR(6) NOT NULL,
    name VARCHAR(255) NOT NULL,
    market_name INTEGER NOT NULL,
    is_splited_stock INTEGER SET DEFAULT 0,
    splited_date DATE, 
);

CREATE TABLE public.searchedStock
(
    searched_stock_key SERIAL PRIMARY KEY,
    stock VARCHAR(255) NOT NULL,
);