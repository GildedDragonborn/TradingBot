import robin_stocks as rh
import alpaca.trading as al
#import alpaca_py as al
import numpy as np
import pandas as pd
import time
import pyotp

# APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

apiKey = ""
secretKey = ""
trading_client = al.client.TradingClient(apiKey, secretKey, paper=True)
account = trading_client.get_account()

if account.trading_blocked:
    print('Account is currently restricted from trading.')

#Total Income
print('${} is available as buying power.'.format(account.buying_power))

#Change in balance between current day and last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')

search_params = al.requests.GetAssetsRequest(asset_class=al.enums.AssetClass.US_EQUITY)
assets = trading_client.get_all_assets(search_params)
#print(assets)



#The segment below is old code accessing robinhood, kept for future use
"""u: str = ''
p: str = ''
t: str = ''

with open('login.txt', "r") as inFile:
    t = inFile.readline()
    u = inFile.readline()
    p = inFile.readline()
totp  = pyotp.TOTP("").now()
login = rh.robinhood.login(u, p, mfa_code=totp)

currStocks = rh.robinhood.build_holdings()
for key,val in currStocks.items(): # Prints all current holdings
    print(key,val)
    print() # Spacing between items
print("done")"""

# Look into https://alpaca.markets/docs/ , has paper-trading which allows for training bot, doesn't account for dividends
# market impact, slippage, fees, and doesn't allow for daytrading for account value under 25k. BUT gives a free 100k balance as default
