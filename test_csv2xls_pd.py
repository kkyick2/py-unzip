import pandas as pd
import xlsxwriter

f_csv = '/home/col/projects/python/py-unzip_script/report_dir/raw4/WEB_2023-09-20.csv'
f_xlsx = f_csv[:-4] + '.xlsx'

print(f'### Script to convent csv to xlsx: {f_csv}')

try:
    #df = pd.read_csv(f_csv, on_bad_lines='skip')
    df = pd.read_csv(f_csv, header=None, on_bad_lines='skip', skip_blank_lines=False)
    print(f' read csv')
except pd.errors.EmptyDataError:
    print(f' Empty csv')
    df = pd.DataFrame() #create a empty dataframe

print(df)
print(df.columns.tolist())
df.to_excel(f_xlsx)
print(f' convent from csv to xlsx: {f_xlsx}')