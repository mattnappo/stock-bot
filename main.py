import os, sys, json
from src.portfolio import Portfolio
from src.spreadsheet import Spreadsheet

class StockBot:
    def __init__(self):
        self.portfolio = { }
        self.p = Portfolio()
        self.s = Spreadsheet(self.portfolio)

        self.main()

    def getPortfolio(self):
        self.p = Portfolio()
        self.portfolio = self.p.GetPortfolio()

    def generateSpreadsheet(self):
        self.getPortfolio()
        self.s = Spreadsheet(self.portfolio)
        self.s.FillSpreadsheet()

    def buy(self, ticker, shares, price):
        portfolio = ""
        with open("data/portfolio.json", "r") as f:
            portfolio = f.read()
        portfolio = json.loads(portfolio)

        order = {
            ticker: {
                "buyPrice": str(price),
                "shares": shares
            }
        }
        
        portfolio.update(order)

        with open("data/portfolio.json", "w") as f:
            json.dump(portfolio, f)

    def sell(self, ticker, shares):
        portfolio = ""
        with open("data/portfolio.json", "r") as f:
            portfolio = f.read()
        portfolio = json.loads(portfolio)

        if not (ticker in portfolio):
            return "You don't own any " + ticker + "."
        
        currentShares = int(portfolio[ticker]["shares"])

        if currentShares < shares:
            return "You don't own enough shares to sell " + str(shares) + "."

        order = {
            ticker: {
                "buyPrice": portfolio[ticker]["buyPrice"],
                "shares": currentShares - int(shares)
            }
        }
        
        portfolio.update(order)

        with open("data/portfolio.json", "w") as f:
            json.dump(portfolio, f)

        buyPrice  = float(portfolio[ticker]["buyPrice"])
        sellPrice = round((float(self.p.getStockData(ticker)[ticker.upper()]["currentPrice"][1:])), 2)
        profit    = round(((sellPrice - buyPrice) * shares), 2)

        message = "Sold " + str(shares) + " shares of " + ticker + " for $" + str(sellPrice) + ".\n"
        message += "You made $" + str(profit) + "."
        return message
    def main(self):
        buffer = "Welcome to StockBot v1.0!\nOptions:"
        while True:
            os.system("clear")
            print(buffer)
            buffer = ""

            print("[1] Generate a report")
            print("[2] Buy")
            print("[3] Sell")
            print("[E] Exit")

            command = input("> ").lower()
            if command == "1":
                self.generateSpreadsheet()
                buffer = "Spreadsheet has been generated."

            elif command == "2":
                print("What is the ticker?")
                ticker = input("> ")

                shares = 0
                print("How many shares to buy?")
                try:
                    shares = int(input("> "))
                except Exception:
                    buffer = "That is not a valid amount of shares."
                
                price = 0.0
                print("Price to buy at?")
                try:
                    price = float(input("> "))
                    self.buy(ticker, shares, price)
                except Exception:
                    buffer = "That is not a valid price."

                buffer = "Bought " + str(shares) + " shares of " + ticker + " for $" + str(price) + "."

            elif command == "3":
                print("What is the ticker?")
                ticker = input("> ")

                shares = 0
                print("How many shares to sell?")
                try:
                    shares = int(input("> "))
                except ValueError:
                    buffer = "That is not a valid amount of shares."
                    continue
                buffer = self.sell(ticker, shares)

            elif command == "e":
                print("Thank you for using StockBot!")
                sys.exit(-1)
            
            else:
                buffer = "Unknown command."

sb = StockBot()