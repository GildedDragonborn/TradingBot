import robin_stocks as rh
import numpy as np
import pandas as pd
import time
import pyotp

u: str = ''
p: str = ''
t: str = ''

with open('login.txt', "r") as inFile:
    t = inFile.readline()
    u = inFile.readline()
    p = inFile.readline()
    print(t)
totp  = pyotp.TOTP(t).now()
login = rh.robinhood.login(u, p, mfa_code=totp)

currStocks = rh.robinhood.build_holdings()
for key,val in currStocks.items(): # Prints all current holdings
    print(key,val)
    print() # Spacing between items
print("done")

# Look into https://alpaca.markets/docs/ , has paper-trading which allows for training bot, doesn't account for dividends
# market impact, slippage, fees, and doesn't allow for daytrading for account value under 25k. BUT gives a free 100k balance as default
