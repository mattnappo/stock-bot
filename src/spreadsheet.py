import json, datetime
import xlwt

class Spreadsheet:
    def __init__(self, stockData):
        self.timestamp = datetime.datetime.now().strftime("%A, %d.x %B %Y %I:%M%p")

        fileDate = datetime.datetime.now().strftime("%m_%d_%Y")
        self.spreadsheetName = "reports/" + fileDate + ".xlsx"

        self.stockData = stockData

        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet("Report")
        
        self.headerStyle = xlwt.easyxf("font: name Times New Roman, color-index black, bold on")
        
        self.blackDataStyle   = xlwt.easyxf(
            "font: name Times New Roman, color-index black",
            num_format_str="#,##0.00"
        )

        self.redDataStyle   = xlwt.easyxf(
            "font: name Times New Roman, color-index red",
            num_format_str="#,##0.00"
        )

        self.greenDataStyle   = xlwt.easyxf(
            "font: name Times New Roman, color-index green",
            num_format_str="#,##0.00"
        )

        self.setupHeaders()

    def setupHeaders(self):
        self.ws.write(0, 0, "Matt's Daily Stock Reports", self.headerStyle)
        self.ws.write(1, 0, self.timestamp, self.headerStyle)

        self.ws.write(3, 0, "Ticker", self.headerStyle)
        self.ws.write(3, 1, "# of Shares", self.headerStyle)

        self.ws.write(3, 2, "Buy Price", self.headerStyle)
        self.ws.write(3, 3, "Current Price", self.headerStyle)

        self.ws.write(3, 4, "$ Change", self.headerStyle)
        self.ws.write(3, 5, "% Change", self.headerStyle)
        
        self.ws.write(3, 6, "Profit", self.headerStyle)

    def fillRow(self, ticker, row):
        stock = self.stockData[ticker]
        print()
        print()
        print(stock)
        print()
        print()
        buyPrice     = stock["buyPrice"]
        currentPrice = stock["currentPrice"]
        shares       = stock["shares"]
        profit       = stock["profit"]

        percentChange = stock["percentChange"]
        dollarChange  = stock["dollarChange"]

        self.ws.write(row, 0, ticker, self.blackDataStyle)
        self.ws.write(row, 1, shares, self.blackDataStyle)

        self.ws.write(row, 2, buyPrice, self.blackDataStyle)
        self.ws.write(row, 3, currentPrice, self.blackDataStyle)

        if dollarChange[0] == "-":
            dollarChange = "$" + dollarChange[1:]
            self.ws.write(row, 4, dollarChange, self.redDataStyle)
        else:
            dollarChange = "$" + dollarChange[1:]
            self.ws.write(row, 4, dollarChange, self.greenDataStyle)

        if percentChange[0] == "-":
            self.ws.write(row, 5, percentChange[1:] + "%", self.redDataStyle)
        else:
            self.ws.write(row, 5, percentChange[1:] + "%", self.greenDataStyle)

        if profit[0] == "-":
            profit = "$" + profit[1:]
            self.ws.write(row, 6, profit, self.redDataStyle)
        else:
            self.ws.write(row, 6, "$" + profit, self.greenDataStyle)
    
    def fillTotal(self, row):
        total          = self.stockData["total"]
        totalPercentUp = str(total["percentUp"])
        totalDollarsUp = str(total["dollarsUp"])

        positiveDollars = total["positiveDollars"]
        positivePercent = total["positivePercent"]

        self.ws.write(row, 0, "Total", self.blackDataStyle)

        if positivePercent:
            self.ws.write(row, 1, totalPercentUp + "%", self.greenDataStyle)
        else:
            self.ws.write(row, 1, totalPercentUp + "%", self.redDataStyle)

        if positiveDollars:
            self.ws.write(row, 2, "$" + totalDollarsUp, self.greenDataStyle)
        else:
            self.ws.write(row, 2, "$" + totalDollarsUp, self.redDataStyle)

    def FillSpreadsheet(self):
        print("start")
        print(self.stockData)
        print("end")
        row = 4
        for stock in self.stockData:
            print("stock: " + stock)
            if stock != "total":
                self.fillRow(stock, row)
                row += 1
        self.fillTotal(row + 2)

        self.wb.save(self.spreadsheetName)