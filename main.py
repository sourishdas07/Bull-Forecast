import pandas as pd
import pandas_datareader
import datetime as dt
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import time
from textblob import TextBlob


ticker = input("Enter a ticker: ")

start_date = dt.datetime(2020, 1, 1)
end_date = dt.datetime(2022, 7, 30)
stock_info = pandas_datareader.DataReader(
    ticker, 'yahoo', start_date, end_date)

data = stock_info[['Close']]
data = data.rename(columns={'Close': 'True_Close'})
data['Target'] = stock_info.rolling(2).apply(
    lambda x: x.iloc[1] > x.iloc[0])['Close']

predictors = ['Close', 'High', 'Low', 'Open', 'Volume']
stock_prev = stock_info.copy()
stock_prev = stock_prev.shift(1)
cut_off = 1
data = data.join(stock_prev[predictors]).iloc[cut_off:]


# Part 3
estimators = 500  # number of decision trees
samples_split = 3  # minimum number of samples required before split
model = RandomForestClassifier(
    n_estimators=estimators, min_samples_split=samples_split, random_state=1)


# Part 4
pred_days = 200
train = data.iloc[:-pred_days]
test = data.iloc[-pred_days:]

model.fit(train[predictors], train['Target'])

# Part 5
preds = (model.predict_proba(test[predictors]))[:, 1]
preds = pd.Series(preds, index=test.index)
target_precision = 0.8
preds[preds >= target_precision] = 1
preds[preds < target_precision] = 0


# Part 6
combined = pd.concat({'Target': test['Target'], 'Predictions': preds}, axis=1)
plt.plot(combined['Predictions'])
plt.plot(combined['Target'])
plt.show()