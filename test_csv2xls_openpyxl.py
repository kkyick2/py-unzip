from openpyxl import Workbook
import csv

f_csv = '/home/col/projects/python/py-unzip_script/report_dir/raw4/IPS_2023-08-26.csv'
f_xlsx = f_csv[:-4] + '.xlsx'

print(f'### Script to convent csv to xlsx: {f_csv}')

try:
    wb = Workbook()
    ws = wb.active
    with open(f_csv, 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(f_xlsx)
except Exception:
    print(f' Empty csv')

print(f' convent from csv to xlsx: {f_xlsx}')