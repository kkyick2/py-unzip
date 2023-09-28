import pandas as pd
import xlsxwriter

f_csv = '/home/col/projects/python/py-unzip_script/upload/T001/DNS_2023-09-23.csv'
f_xlsx = f_csv[:-4] + '.xlsx'

try:
    df = pd.read_csv(f_csv)
except pd.errors.EmptyDataError:
    df = pd.DataFrame() #create a empty dataframe
df.to_excel(f_xlsx, index=False)