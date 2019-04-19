import json, requests

class Portfolio:
    def __init__(self):
        self.stockData = {}

        self.portfolio = {}
        self.loadPortfolio()

        self.APIKey = ""
        self.loadAPIKey()
    
    def loadPortfolio(self):
        with open("data/portfolio.json", "r") as f:
            self.portfolio = json.load(f)

    def loadAPIKey(self):
        with open("data/api_key", "r") as f:  
            self.APIKey = f.read()
    
    def calculate(self, buyPrice, currentPrice, ticker):
        dollarChange  = round((currentPrice - buyPrice), 2)
        percentChange = round(((dollarChange / abs(buyPrice)) * 100), 2)

        if str(dollarChange)[0] == "-":
            dollarChange = "-" + str(dollarChange)[1:]
        else:
            dollarChange = "+" + str(dollarChange)

        if str(percentChange)[0] == "-":
            percentChange = str(percentChange)
        else:
            percentChange = "+" + str(percentChange)

        shares = str(self.portfolio[ticker]["shares"])
        profit = str(round((float(shares) * float(dollarChange)), 2))

        jsonChange = {
            "dollars": dollarChange,
            "percent": percentChange,
            "shares": shares,
            "profit": profit
        }

        return jsonChange

    def parseResponse(self, response):
        quote = response["Global Quote"]

        ticker       = quote["01. symbol"]
        currentPrice = quote["05. price"]

        currentPrice = round(float(currentPrice), 2)
        buyPrice = self.portfolio[ticker.lower()]["buyPrice"]

        calculations = self.calculate(float(buyPrice), float(currentPrice), ticker.lower())
        dollarChange  = calculations["dollars"]
        percentChange = calculations["percent"]

        shares = calculations["shares"]
        profit = calculations["profit"]

        jsonStockReport = {
            ticker: {
                "buyPrice": "$" + str(buyPrice),
                "currentPrice": "$" + str(currentPrice),
                "dollarChange": dollarChange,
                "percentChange": percentChange,
                "shares": shares,
                "profit": profit
            }
        }
        return jsonStockReport

    def getStockData(self, ticker):
        request = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" \
            + ticker.upper() + "&apikey=" + self.APIKey
        # print(request)

        response = requests.get(request)
        print(response.json())

        jsonStockReport = self.parseResponse(response.json())
        print(jsonStockReport)

        return jsonStockReport

    def GetPortfolio(self):
        for ticker in self.portfolio:
            jsonStockReport = self.getStockData(ticker)
            self.stockData.update(jsonStockReport)
        return self.stockData