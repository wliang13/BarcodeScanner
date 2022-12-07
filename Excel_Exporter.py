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

def exportExcelSheet(elData):
    # Creates the xlsx file and dates it
    sTime = datetime.now().strftime("%H-%M-%S_-""_%m-%d-%Y")
    sDocumentName = 'BarcodeIndex-_' + sTime + '_.xlsx'
    xlsxWorkbook = xlsxwriter.Workbook(sDocumentName)
    xlsxWorksheet = xlsxWorkbook.add_worksheet()

    # Adds the bold font, use 'italics' or others in this section
    bold = xlsxWorkbook.add_format({'bold': True})

    # Header Goes Data Here If more is needed, this uses Row-Column as string in first argument.
    xlsxWorksheet.write('A1', 'Code', bold)
    xlsxWorksheet.write('B1', 'Item', bold)
    xlsxWorksheet.write('C1', 'Exp. D', bold)

    """
    # Test Input
    elData = [
        ['12349912', 'Tomatoes', '11/12'],
        ['12747912', 'Carrots', '09/10'],
        ['12851573', 'Cheese', '02/12']
    ]
    """

    # iteration could be optimized dont bother
    iRow = 1
    iCol = 0
    for i, j, k in elData:
        xlsxWorksheet.write(iRow, iCol, i)
        xlsxWorksheet.set_column(iRow, iCol, 15)
        xlsxWorksheet.write(iRow, iCol + 1, j)
        xlsxWorksheet.write(iRow, iCol + 2, k)
        iRow += 1

    xlsxWorksheet.close()
