import json, datetime
import xlwt

class SpreadsheetManager:
    def __init__(self, stockData):
        self.timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        self.spreadsheetName = "report.xlsx"

        self.stockData = stockData

        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet("Report")
        
        self.headerStyle = xlwt.easyxf("font: name Times New Roman, color-index black, bold on")
        self.dataStyle   = xlwt.easyxf("font: name Times New Roman, color-index black")

        self.setupHeaders()

    def setupHeaders(self):
        self.ws.write(0, 0, "Matt's Daily Stock Reports", self.headerStyle)
        self.ws.write(1, 0, self.timestamp, self.headerStyle)

        self.ws.write(3, 0, "Ticker", self.headerStyle)
        self.ws.write(3, 1, "Open Price", self.headerStyle)
        self.ws.write(3, 2, "Current Price", self.headerStyle)

        self.ws.write(3, 3, "% Change", self.headerStyle)
        self.ws.write(3, 4, "$ Change", self.headerStyle)

    def fillRow(self, ticker, row):
        stock = self.stockData[ticker]
        
        openPrice    = stock["openPrice"]
        currentPrice = stock["currentPrice"]

        percentChange = stock["percentChange"]
        dollarChange  = stock["dollarChange"]

        self.ws.write(row, 0, ticker, self.dataStyle)

        self.ws.write(row, 1, openPrice, self.dataStyle)
        self.ws.write(row, 0, currentPrice, self.dataStyle)

        self.ws.write(row, 0, ticker, self.dataStyle)
        self.ws.write(row, 0, ticker, self.dataStyle)

    def FillSpreadsheet(self):
        print("start")
        print(self.stockData)
        print("end")
        row = 0
        for stock in self.stockData:
            self.fillRow(stock, row)
            row += 1

        self.wb.save(self.spreadsheetName)