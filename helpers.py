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
        #break         
    
    data_list = []
    for i in data.index:
        data_list.append(data["Adj Close"][i])

    N = len(data_list)
##    total_close = sum(list)
##    print(total_close)
    
    old_close = data_list[0]
##    print(old_close)

    for i in range(1,10):
        print(data_list[i])
        
    daily_return_accum = 0
    daily_return_squared_accum = 0
    

    for i in range(1,N):
        #print(f"i is {i}", end = "  ")
        #print(f"list ith element is {list[i]}",end="  ")
        #print(f"Old close is {old_close}", end = "  ")
        
        price_relative = data_list[i]/old_close
        #print(f"Price relative is {price_relative}", end ="  ")
        
        daily_return = log(price_relative)
        #print(f"Daily return is {daily_return}", end ="  ")
        daily_return_accum += daily_return
        
        daily_return_squared = daily_return * daily_return
        #print(f"Daily return squared is {daily_return_squared}", end ="  ") 
        daily_return_squared_accum += daily_return_squared

        old_close = data_list[i]
        #print(f"Old close is {old_close}", end = "  ")
        #print()
    
        if i == N-1:
            break
    results_dict = {}
    #print(f"N: {N}")
    NewN = N - 1    
    st_dev_daily = sqrt((daily_return_squared_accum/(NewN))-((daily_return_accum*daily_return_accum)/((NewN)*N)))
    #print(f"Daily return squared total: {daily_return_squared_accum}")
    #print(f"Daily return total: {daily_return_accum}")
    #print(f"Standard deviation daily: {st_dev_daily}")
    historical_volatility = st_dev_daily*(sqrt(N/term))
    results_dict["historical_volatility"] = historical_volatility
    
    #print(f"HIstorical Volatility: {historical_volatility}")  

    variance = (historical_volatility * historical_volatility) 
    #print(f"Variance: {variance}")
    d1 = (log(stock_price/strike_price) + ((risk_free_rate/100) - dividend_yield_percentage +(variance/2) * term))/((sqrt(variance))*(sqrt(term)))      
    #print(f"D1: {d1}")
    N_d1 = norm.cdf(d1, 0, 1)
    #print(f"N(d1): {N_d1}")
    d2 = d1 - ((sqrt(variance))*(sqrt(term)))
    N_d2 = norm.cdf(d2, 0, 1)
    #print(f"d2: {d2}")
    #print(f"N(d2): {N_d2}")
    
    call_value = (exp((0 - dividend_yield_percentage) * term))*N_d1*stock_price - strike_price*(exp(0 - (risk_free_rate/100)))*N_d2
    #print(f"Per option call value: {call_value}")
    results_dict["call_value"] = call_value 
    fair_value_option = round(number_of_options * call_value,2)
    #print(f"The fair value of the options are {fair_value_option}")
    results_dict["fair_value_option"] = fair_value_option

    return results_dict
      
           
