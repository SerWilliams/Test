'''
import xlrd, xlwt
book = xlrd.open_workbook('D:\\raschet.xlsx')
sheet = book.sheet_by_index(0)
print('Rows',sheet.nrows)
data = [sheet.row_values(i) for i in range(sheet.nrows)]
nbook = xlwt.Workbook()
nsheet = nbook.add_sheet('Лист 101')
for s in range(len(data)):
    for r in range(len(data[s])):
        nsheet.write(s, r, data[s][r])

nbook.save('D:\\copy_raschet.xls')

import xlsxwriter

book = xlsxwriter.Workbook('D:\\test.xlsx')
sheet1 = book.add_worksheet()
sheet2 = book.add_worksheet()

sheet1.write(0, 0, 123)
'''

import csv, xlwt, os
book = xlwt.Workbook()
sheet = book.add_sheet('Raschet')
with open(r'D:\raschet.csv') as filecsv:
    readf = csv.reader(filecsv, delimiter = ';',skipinitialspace = True)
    str = 0
    for line in readf:
        for j in range(len(line)):
            sheet.write(str, j, line[j])
        str += 1
book.save(r'D:\New_raschet.xls')


