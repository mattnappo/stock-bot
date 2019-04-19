import json
from src.portfolio import Portfolio
from src.spreadsheet import Spreadsheet

# Get the stock prices
p = Portfolio()
portfolio = p.GetPortfolio()

# stockData = {'AMZN': {'openPrice': 1868.79, 'currentPrice': 1861.69, 'dollarChange': '+$7.1', 'percentChange': '-0.38%'}, 'SPY': {'openPrice': 290.1, 'currentPrice': 289.99, 'dollarChange': '-$0.11', 'percentChange': '-0.04%'}}

print()
print()
print()

print(portfolio)

# Generate the spreadsheet
s = Spreadsheet(portfolio)
s.FillSpreadsheet()