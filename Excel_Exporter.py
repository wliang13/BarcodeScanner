import xlsxwriter
from datetime import datetime


# USAGE
# Add to the app.py, 'from Excel_Exporter import exportExcelSheet'.
# Function takes in 2D enumerator lists, check headers to see in what order.
# You will need xlsxwriter.py in your interpreter to compile.
#
# todo
# Add button on html to just do this function.
# Find everything the barcode exports and add to headers here.

def exportExcelSheet(entries):
    # Creates the xlsx file and dates it
    sTime = datetime.now().strftime("%H-%M-%S_-""_%m-%d-%Y")
    sDocumentName = 'BarcodeIndex-_' + sTime + '_.xlsx'
    xlsxWorkbook = xlsxwriter.Workbook(sDocumentName)
    xlsxWorksheet = xlsxWorkbook.add_worksheet()
    date_format = xlsxWorkbook.add_format({'num_format': 'mm/dd/yyyy hh:mm'})
    xlsxWorksheet.set_column(3,4,20)

    # Adds the bold font, use 'italics' or others in this section
    bold = xlsxWorkbook.add_format({'bold': True})

    # Header Goes Data Here If more is needed, this uses Row-Column as string in first argument.
    xlsxWorksheet.write('A1', 'Factory', bold)
    xlsxWorksheet.write('B1', 'Building', bold)
    xlsxWorksheet.write('C1', 'Row', bold)
    xlsxWorksheet.write('D1', 'Date Added', bold)
    xlsxWorksheet.write('E1', 'Barcode', bold)

    iRow = 1
    iCol = 0
    for entry in entries:
        xlsxWorksheet.write(iRow, iCol, entry.factory)
        xlsxWorksheet.write(iRow, iCol+1, entry.building)
        xlsxWorksheet.write(iRow, iCol+2, entry.content)
        xlsxWorksheet.write(iRow, iCol+3, entry.date_created, date_format)
        xlsxWorksheet.write(iRow, iCol+4, entry.barcode)
        iRow += 1

    xlsxWorkbook.close()

