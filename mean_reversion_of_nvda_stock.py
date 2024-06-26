# -*- coding: utf-8 -*-
"""Mean Reversion of NVDA Stock.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PjjKbGn4DHdz8bMITxdzphlaKF4ehpJ0

Mean Reversion Trading Strategy on NVDA Stock
"""

#Description: Mean Reversion Trading Strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from google.colab import files
files.upload()

df = pd.read_csv('NVDA.csv')
#date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
df.drop(['Date'], inplace = True, axis =1 )
df

#SMA: Simple Moving Average

def SMA(data, period = 30, column = 'Close'):
  return data[column].rolling(window = period).mean()

df['SMA'] = SMA(df, 21)
df['Simple_Returns'] = df.pct_change(1)['Close']
df['Log_Returns'] = np.log(1+df['Simple_Returns'])
df['Ratios'] = df['Close'] / df['SMA']
df

df['Ratios'].describe()

percentiles = [15,20,50,80,85]
ratios = df['Ratios'].dropna()
percentile_value = np.percentile(ratios, percentiles)
percentile_value

plt.figure(figsize =(14,7))
plt.title('Ratios')

df['Ratios'].dropna().plot(legend = True)
plt.axhline(percentile_value[0], c='green', label = '15th Percentile')
plt.axhline(percentile_value[2], c='yellow', label = '50th Percentile')
plt.axhline(percentile_value[-1], c='red', label = '85th Percentile')

#buy and sell signals

sell = percentile_value[-1] #85th
buy= percentile_value[0] #15th

df['Positions'] = np.where(df.Ratios > sell, -1, np.nan)
df['Positions'] = np.where(df.Ratios < buy, 1, df['Positions'])

#ffill to fill the missing values
df['Positions'] = df['Positions'].ffill()

df['Buy'] = np.where(df.Positions ==1, df['Close'],np.nan)
df['Sell'] = np.where(df.Positions ==-1, df['Close'],np.nan)

plt.figure(figsize =(14,7))
plt.title('Close Price with Buy & Sell Signals of NVDA')
plt.plot(df['Close'], alpha = 0.5, label = 'Close')
plt.plot(df['SMA'], alpha = 0.5, label ='SMA')
plt.scatter(df.index, df['Buy'],color = 'green', label ='Buy signal', marker = '^', alpha = 1)
plt.scatter(df.index, df['Sell'],color = 'red', label ='Sell signal', marker = 'v', alpha = 1)
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

df['Strategy_Returns'] = df.Positions.shift(1)*df.Log_Returns
df['Strategy_Returns']

plt.figure(figsize =(14,7))
plt.title('Growth of 1 dollar Investment at NVDA Stock')
plt.plot(np.exp(df['Log_Returns'].dropna()).cumprod(), c='green', label = 'Buy/Hold Strategy')
plt.plot(np.exp(df['Strategy_Returns'].dropna()).cumprod(), c='red', label = 'Mean Reversion Strategy')

plt.legend()
plt.show()

#Returns for both strategy
print('Buy & Hold Strategy Returns:', np.exp(df['Log_Returns'].dropna()).cumprod()[-1]-1)
print('Mean Reversion Strategy Returns:', np.exp(df['Strategy_Returns'].dropna()).cumprod()[-1]-1)