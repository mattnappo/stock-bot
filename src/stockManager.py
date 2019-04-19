import json
import requests

class StockManager:
    def __init__(self):
        self.stockData = {}

        self.tickers = {}
        self.loadTickers()

        self.APIKey = ""
        self.loadAPIKey()
    
    def loadTickers(self):
        with open("data/stocks.json", "r") as f:
            self.tickers = json.load(f)

    def loadAPIKey(self):
        with open("data/api_key", "r") as f:  
            self.APIKey = f.read()
    
    def calculateChange(self, openPrice, currentPrice):
        dollarChange = currentPrice - openPrice
        percentChange = (dollarChange / abs(openPrice)) * 100

        jsonChange = {
            "dollars": dollarChange,
            "percent": percentChange
        }

        return jsonChange

    def parseResponse(self, response):
        quote = response["Global Quote"]

        symbol       = quote["01. symbol"]
        openPrice    = quote["02. open"]
        currentPrice = quote["05. price"]

        change = self.calculateChange(openPrice, currentPrice)
        dollarChange  = change["dollars"]
        percentChange = change["percent"]

        jsonStockReport = {
            symbol: {
                "openPrice": openPrice,
                "currentPrice": currentPrice
            }
        }
        return jsonStockReport

    def getPrice(self, ticker):
        # request = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" \
        #     + ticker.upper() + "&apikey=" + self.APIKey

        request = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" \
            + ticker.upper() + "&apikey=" + self.APIKey
        print(request)

        response = requests.get(request)
        print(response.json())

        jsonStockReport = self.parseResponse(response.json())
        return jsonStockReport

    def GetPrices(self):
        for ticker in self.tickers:
            jsonStockReport = self.getPrice(ticker)
            self.stockData.update(jsonStockReport)