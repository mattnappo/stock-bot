import json, datetime
import xlwt

class SpreadsheetManager:
    def __init__(self, stockData):
        self.timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        self.spreadsheetName = "report.xlsx"

        self.stockData = stockData
        self.setupHeaders()

    def setupHeaders(self):
        # spreadsheet = excel.Workbook(self.spreadsheetName)
        # worksheet = spreadsheet.add_worksheet()

        # worksheet.write("B2", "Matt's Daily Stock Report")
        # worksheet.write("C2", self.timestamp)

        # worksheet.write("E2", "Open Price")
        # worksheet.write("E3", "Current Price")

        # worksheet.write("E4", "Dollar Change")
        # worksheet.write("E5", "Percent Change")

        # spreadsheet.Close()


        headerStyle = xlwt.easyxf("font: name Times New Roman, color-index black, bold on")
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook()
        ws = wb.add_sheet("Report")

        ws.write(0, 0, 1234.56, headerStyle)
        ws.write(1, 0, "ok", style1)
        ws.write(2, 0, 1)
        ws.write(2, 1, 1)
        ws.write(2, 2, xlwt.Formula("A3+B3"))
        wb.save('example.xls')