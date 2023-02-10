import robin_stocks as rh
import alpaca.trading as al
import numpy as np
import pandas as pd
import keras as ke
from keras.models import Sequential
from keras.layers import Dense, LSTM
import datetime
import requests
import os
import time
import pyotp

# APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
BASE_URL = 'https://paper-api.alpaca.markets'
ORDERS_URL = '{}/v2/orders'.format(BASE_URL)

with open("login.txt", "r") as inFile:
    apiKey = inFile.readline().strip()
    secretKey = inFile.readline().strip()

HEADERS = {'APCA-API-KEY-ID':apiKey,'APCA-API-SECRET-KEY':secretKey}

closePositions = False

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
positions = trading_client.get_all_positions()

if closePositions: #CLOSES ALL POSITIONS REGARDLESS OF GAIN OR LOSS
    trading_client.close_all_positions(cancel_orders=True)
#print(assets)

#START DEEP LEARNING SECTION

df = pd.read_csv("Stockdata.csv")
stockdata = df[['Open', 'High', 'Low', 'Close', 'Volume']]

stockdata = (stockdata-stockdata.mean()) / stockdata.std() # normalize data

stockdata = np.array(stockdata).reshape(-1, 5) # Convert the data into a numpy array and reshape it for input into the network

# Split the data into training and test sets
x_train = stockdata[:1000]
y_train = df['Close'][:1000]
x_test = stockdata[1000:]
y_test = df['Close'][1000:]

model = Sequential()

model.add(LSTM(32, input_shape=(5, 1), activation='relu', return_sequences=True))
model.add(LSTM(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Fit the model to the training data
model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))

# Make predictions using the predict method
predictions = model.predict(stockdata)

# Print the predictions
print(predictions)

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
