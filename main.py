import os, sys
from src.portfolio import Portfolio
from src.spreadsheet import Spreadsheet

class StockBot:
    def __init__(self):
        self.portfolio = { }
        self.main()

    def getPortfolio(self):
        p = Portfolio()
        self.portfolio = p.GetPortfolio()

    def generateSpreadsheet(self):
        self.getPortfolio()
        s = Spreadsheet(self.portfolio)
        s.FillSpreadsheet()

    def buy(self):
        pass

    def sell(self):
        pass

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

                print("How many shares to buy?")
                try:
                    shares = int(input("> "))
                    self.buy(ticker, shares)
                except:
                    buffer = "That is not a valid amount of shares."

            elif command == "3":
                self.sell()

            elif command == "e":
                print("Thank you for using StockBot!")
                sys.exit(-1)
            
            else:
                buffer = "Unknown command."

sb = StockBot()