import pandas as pd
import xlsxwriter

f_csv = '/home/col/projects/python/py-unzip_script/report_dir/raw3/20231004/DNS_2023-09-25.csv'
f_xlsx = f_csv[:-4] + '.xlsx'

print(f'### Script to convent csv to xlsx: {f_csv}')

try:
    df = pd.read_csv(f_csv, on_bad_lines='skip')
    print(f' read csv')
except pd.errors.EmptyDataError:
    print(f' Empty csv')
    df = pd.DataFrame() #create a empty dataframe

df.to_excel(f_xlsx, index=False)
print(f' convent from csv to xlsx: {f_xlsx}')