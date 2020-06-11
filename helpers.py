import csv
import yfinance as yf
from sys import argv
from math import log, sqrt, exp, ceil
from scipy.stats import norm
from datetime import datetime

def fair_value_function(list):
    term = list[0]
    strike_price = list[1]
    stock_price = list[2]
    risk_free_rate = list[3]
    number_of_options = list[4]
    dividend_yield_percentage = list[5]
    Ticker = list[6]
    Start_date_day = list[7]
    Start_date_month = list[8]
    Start_date_year = list[9]
    Start_date = datetime(Start_date_year,Start_date_month,Start_date_day)
    end_date_day = list[10]
    end_date_month = list[11]
    end_date_year = list[12]
    end_date = datetime(end_date_year,end_date_month,end_date_day)

    data = yf.download(f"{Ticker}",Start_date,end_date)

    if len(data) == 0:
        return "error"

    data_list = []
    for i in data.index:
        data_list.append(data["Adj Close"][i])

    N = len(data_list)

    old_close = data_list[0]


    daily_return_accum = 0
    daily_return_squared_accum = 0


    for i in range(1,N):
        price_relative = data_list[i]/old_close
        daily_return = log(price_relative)
        daily_return_accum += daily_return

        daily_return_squared = daily_return * daily_return
        daily_return_squared_accum += daily_return_squared

        old_close = data_list[i]
        if i == N-1:
            break
    results_dict = {}
    NewN = N - 1
    st_dev_daily = sqrt((daily_return_squared_accum/(NewN))-((daily_return_accum*daily_return_accum)/((NewN)*N)))
    historical_volatility = st_dev_daily*(sqrt(N/term))

    results_dict["historical_volatility"] = (historical_volatility)
    variance = (historical_volatility * historical_volatility)
    d1 = (log(stock_price/strike_price) + ((risk_free_rate/100) - dividend_yield_percentage +(variance/2) * term))/((sqrt(variance))*(sqrt(term)))
    N_d1 = norm.cdf(d1, 0, 1)
    d2 = d1 - ((sqrt(variance))*(sqrt(term)))
    N_d2 = norm.cdf(d2, 0, 1)
    call_value = (exp((0 - dividend_yield_percentage) * term))*N_d1*stock_price - strike_price*(exp(0 - (risk_free_rate/100)))*N_d2
    results_dict["call_value"] = round(call_value,2)
    fair_value_option = round(number_of_options * call_value,2)
    results_dict["fair_value_option"] = fair_value_option

    return results_dict


