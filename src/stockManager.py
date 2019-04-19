import json

class StockManager:
    def __init__(self):
        self.prices = {}

        self.tickers = {}
        self.loadStocks()

        self.APIKey = ""
        self.loadAPIKey()
    
    def loadStocks(self):
        with open("data/stocks.json", "r") as f:  
            json.dump(self.tickers, f)

    def loadAPIKey(self):
        with open("data/api_key", "r") as f:  
            self.APIKey = f.read()

    def getPrice(self, ticker):
        request = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
        + ticker.upper() + "&apikey=" + self.APIKey

    def GetPrices(self):
        for ticker in self.tickers:
            print(ticker)