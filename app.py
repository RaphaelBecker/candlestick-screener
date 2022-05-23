import os, csv
import talib
import yfinance as yf
import pandas
import utils.helpers as hlps
from flask import Flask, escape, request, render_template
from patterns import candlestick_patterns
from ma_rules import sma20_rules, sma50_rules, sma100_rules, sma150_rules, sma200_rules

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            data = yf.download(symbol, start="2020-01-01", end=str(hlps.get_current_date()))
            data.to_csv('datasets/daily/{}.csv'.format(symbol))

    return {
        "code": "success"
    }

@app.route('/')
def index():
    pattern  = request.args.get('pattern', False)
    sma20_rule = request.args.get('sma20_rule', False)
    sma50_rule = request.args.get('sma50_rule', False)
    sma100_rule = request.args.get('sma100_rule', False)
    sma150_rule = request.args.get('sma150_rule', False)
    sma200_rule = request.args.get('sma200_rule', False)
    print(f"pattern: {pattern} sma20_rule: {sma20_rule}")
    stocks = {}

    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir('datasets/daily'):
            df = pandas.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('failed on filename: ', filename)

    return render_template('index.html',
                           candlestick_patterns=candlestick_patterns, pattern=pattern,
                           sma20_rules=sma20_rules, sma20_rule=sma20_rule,
                           sma50_rules=sma50_rules, sma50_rule=sma50_rule,
                           sma100_rules=sma100_rules, sma100_rule=sma100_rule,
                           sma150_rules=sma150_rules, sma150_rule=sma150_rule,
                           sma200_rules=sma200_rules, sma200_rule=sma200_rule,
                           stocks=stocks)
