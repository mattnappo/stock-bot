from src.stockManager import StockManager
from src.spreadsheetManager import SpreadsheetManager

# Get the stock prices
sm = StockManager()
sm.GetPrices()
print()
print()
print()
stockData = sm.stockData
print(stockData)

# Generate the spreadsheet
sm = SpreadsheetManager(stockData)