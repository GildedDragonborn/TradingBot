import robin_stocks as rh
import numpy as np
import pandas as pd
import time

user: str = ""
password: str = ""

login = rh.robinhood.login(user, password)

currStocks = rh.robinhood.build_holdings()
for key,val in currStocks.items(): # Prints all current holdings
    print(key,val)
    print() # Spacing between items
print("done")

# Look into https://alpaca.markets/docs/ , has paper-trading which allows for training bot, doesn't account for dividends
# market impact, slippage, fees, and doesn't allow for daytrading for account value under 25k. BUT gives a free 100k balance as default
