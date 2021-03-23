import math
import pandas as pd
import quandl

quandl.ApiConfig.api_key = "YOUR_API_KEY"
data = quandl.get("BITFINEX/BTCUSD", start_date="2017-01-01")

df = pd.DataFrame(data=data)
df['Close'] = pd.to_numeric(df['Last'], downcast='float')
df['Returns'] = df['Close'].pct_change()
del df['High']
del df['Low']
del df['Mid']
del df['Bid']
del df['Ask']
del df['Volume']
del df['Last']

df['10DMA'] = df['Close'].rolling(window=10).mean()
df['20DMA'] = df['Close'].rolling(window=20).mean()

df = df.drop(df.index[0:19])
df = df.dropna()

## Backtesting

df['Signal'] = df['10DMA'] > df['20DMA']

df['Signal2'] = df['Signal'].shift(1)
print(df['Signal'].value_counts())

df['StrategyReturns'] = df['Signal2'] * df['Returns']
df['Buy & Hold Bitcoin'] = 100 * (1 + df['Returns']).cumprod()
df['Strat'] = 100 * (1 + ( df['Signal'].shift(1) * df['Returns'] )).cumprod()
ax = df[['Strat', 'Buy & Hold Bitcoin']].plot(kind='line', title="Strategy vs Hold Bitcoin")

b = round(df['Buy & Hold Bitcoin'].iloc[-1], 2)
s = round(df['Strat'].iloc[-1], 2)
t = round(((b - 100) / 100) * 100, 2)
r = round(((s - 100) / 100) * 100, 2)
print("Buy and hold Bitcoin, from 100$ to " + str(b) + "$" + " performance of " + str(t) + " %")
print("Strategy, from 100$ to " + str(s) + "$" + " performance of " + str(r) + " %")
c = round(r - t, 2)
print("Strategy outperforms Bitcoin by " + str(c) + " %")

## Performance metrics

returnsbtc = t / 100
returnsstrat = r / 100
returnsbtc = returnsbtc ** (1/3.46) - 1
returnsstrat = returnsstrat ** (1/3.46) - 1
volbtc = df['Returns'].std()* math.sqrt(365)
volstrat = df['StrategyReturns'].std()* math.sqrt(365)
print("Volatility Bitcoin " + str(volbtc))
print("Volatility Strategy " + str(volstrat))
sharpebtc = returnsbtc / volbtc
sharpestrat = returnsstrat / volstrat
print("Sharpe Ratio Bitcoin " + str(sharpebtc))
print("Sharpe Ratio Strategy " + str(sharpestrat))
