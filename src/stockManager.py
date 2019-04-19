import json

class StockManager:
    def __init__(self):
        self.tickers = {}
        self.loadStocks()

    def loadStocks(self):
        with open("data/stocks.json", "r") as f:  
            json.dump(self.tickers, f)

    