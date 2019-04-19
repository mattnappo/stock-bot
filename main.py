import json
from src.stockManager import StockManager
from src.spreadsheetManager import SpreadsheetManager

# Get the stock prices
sm = StockManager()
# sm.GetPrices()
print()
print()
print()

# stockData = sm.stockData
stockData = {'AMZN': {'openPrice': 1868.79, 'currentPrice': 1861.69, 'dollarChange': '-$7.1', 'percentChange': '-0.38%'}, 'SPY': {'openPrice': 290.1, 'currentPrice': 289.99, 'dollarChange': '-$0.11', 'percentChange': '-0.04%'}}

print(stockData)

# Generate the spreadsheet
sm = SpreadsheetManager(stockData)
sm.FillSpreadsheet()