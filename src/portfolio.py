import json, requests, sys

class Portfolio:
    def __init__(self):
        self.stockData = {}

        self.portfolio = {}
        self.loadPortfolio()

        self.APIKey = ""
        self.loadAPIKey()

        self.upDollars   = [ ]
        self.downDollars = [ ]
        
        self.upPercentages   = [ ]
        self.downPercentages = [ ]
    
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

        if float(percentChange) >= 0:
            self.upPercentages.append(float(percentChange))
        else:
            self.downPercentages.append(float(percentChange))

        jsonChange = {
            "dollars": dollarChange,
            "percent": percentChange,
            "shares": shares,
            "profit": profit
        }

        return jsonChange

    def calculateTotal(self, ups, downs):
        totalUp = 0
        for up in ups:
            totalUp += up

        totalDown = 0
        for down in downs:
            totalDown += down

        return round((totalUp + totalDown), 2)

    def calculateNet(self):
        totalDollarsUp = self.calculateTotal(
            self.upDollars,
            self.downDollars
        )
        
        totalPercentUp = self.calculateTotal(
            self.upPercentages,
            self.downPercentages
        )

        positiveDollars = False
        if totalDollarsUp >= 0:
            positiveDollars = True
        
        positivePercent = False
        if totalPercentUp >= 0:
            positivePercent = True

        response = {
            "total": {
                "dollarsUp": totalDollarsUp,
                "percentUp": totalPercentUp,
                "positiveDollars": positiveDollars,
                "positivePercent": positivePercent
            }
        }
        return response

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

        if float(profit) >= 0:
            self.upDollars.append(float(profit))
        else:
            self.downDollars.append(float(profit))

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

        response = requests.get(request)

        try:
            jsonStockReport = self.parseResponse(response.json())
        except:
            print("You've reached your maximum amount of API calls per minute.")
            sys.exit(-1)

        return jsonStockReport

    def GetPortfolio(self):
        for ticker in self.portfolio:
            jsonStockReport = self.getStockData(ticker)
            self.stockData.update(jsonStockReport)
        self.stockData.update(self.calculateNet())

        return self.stockData