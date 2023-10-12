import os
import glob
import csv
from xlsxwriter.workbook import Workbook

# method1, input one csv
f_csv = '/home/col/projects/python/py-unzip_script/report_dir/raw4/WEB_2023-09-20.csv'
f_xlsx = Workbook(f_csv[:-4] + '.xlsx')
worksheet = f_xlsx.add_worksheet()
with open(f_csv, 'rt', encoding='utf8') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            worksheet.write(r, c, col)
f_xlsx.close()


'''
# method2, glob whole dir
f_path = '/home/col/projects/python/py-unzip_script/report_dir/raw4'
for f_csv in glob.glob(os.path.join(f_path, '*.csv')):
    f_xlsx = Workbook(f_csv[:-4] + '.xlsx')
    worksheet = f_xlsx.add_worksheet()
    with open(f_csv, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    f_xlsx.close()
'''