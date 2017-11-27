import csv, xlsxwriter, sys, time

'''
Модуль конвертирует cvs файл в xlsx.
Принимает обязательные параметры:
    имя файла csv
    имя файла xlsx
Не обязательные:
    кол-во строк заголовка (выделяется жирным шрифтом и центруется) по умолчанию 1
    кол-во строк подвала (выделяется жирным шрифтом) по умолчанию 7
    знак разделитель (по умолчанию ';')
    Пример:
    csv_to_xsl.py file.csv file.xlsx 2 7 ;
'''


def writ_data(sheet, data, format_cell, start=0, *args):
    try:
        end = args[0]
    except:
        end = len(data)
    for i in range(start, end):
        for j in range(len(data[i])):
            if data[i][j].isdigit():
                sheet.write(i, j, int(data[i][j]), format_cell)
            else:
                sheet.write(i, j, data[i][j], format_cell)


def convert_csv(csvfile, xlsfile, headers, bottom, delim):
    try:
        with open(csvfile) as f:
            rf = csv.reader(f, delimiter=delim, skipinitialspace=True)
            data = [i for i in rf]
            wight_col = [0] * len(data[1])  # Делаем список max кол-ва символов в столбцах
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if wight_col[j] < len(data[i][j]):
                        wight_col[j] = len(data[i][j]) + 3
            book = xlsxwriter.Workbook(xlsfile)
            sheet = book.add_worksheet('KSO_GM')
            format_header = book.add_format({'bold': True, 'align': 'center','border': 1})
            format_body = book.add_format({'align': 'center', 'border': 1})
            format_bottom = book.add_format({'bold': True, 'border': 1})
            for i, width in enumerate(wight_col): # Форматируем ширину столбцов
                sheet.set_column(i, i, width)
            writ_data(sheet, data, format_header, 0, headers)  # Пишем шапку
            writ_data(sheet, data, format_body, start=headers)  # Пишем массив
            writ_data(sheet, data, format_bottom, start=len(data) - bottom)  # Пишем подвал
            book.close()
    except Exception as e:
        print(e)
        time.sleep(5)
    else:
        print('Completed successfuly!')


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError('Not parameters. Exit.')
        elif len(sys.argv) < 4:
            csvfile, xlsfile = sys.argv[1:]
            headers, bottom, delim = 2, 7, ';'
        else:
            csvfile, xlsfile, headers, bottom, delim = sys.argv[1:]
            print('Start convert file {0} to file {1}'.format(csvfile, xlsfile))
    except ValueError as e:
        print(e)
        time.sleep(5)
    else:
        convert_csv(csvfile, xlsfile, int(headers), int(bottom), delim)
