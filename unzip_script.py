import sys,os,re,zipfile,time
from datetime import datetime
import pandas as pd
import xlsxwriter
# kkyick2, 20230928, for hkstp
# === How to use ===
# method1: Usage: python unzip_script.py <full_root_path_to_process>
# method2: create a cron job with 'crontab -e' and verify with 'crontab -l'
#
# === Description ===
# This script reead below folder structure, unzip pattern "xxxReport-YYYY-MM-DD-HHMM_SSSS.zip" and rename to "xxxReport-YYYY-MM-DD.csv"
# Before:
# report_dir
# |--- T001
#      |--- T001-DNS-2023-02-14-1704_1915.zip
#      |--- T001-IPS-2023-02-14-1704_1915.zip
#      |--- T001-WEB-2023-02-14-1704_1915.zip
# |--- T002
#      |--- T001-DNS-2023-02-14-1704_1915.zip
#      |--- T002-IPS-2023-02-14-1704_1915.zip
#      |--- T003-WEB-2023-02-14-1704_1915.zip
#
# After:
# report_dir
# |--- T001
#      |--- DNS_2023-02-14.csv
#      |--- IPS_2023-02-14.csv
#      |--- WEB_2023-02-14.csv
# |--- T002
#      |--- DNS_2023-02-14.csv
#      |--- IPS_2023-02-14.csv
#      |--- WEB_2023-02-14.csv
#
# Convent the csv to xlsx
# report_dir
# |--- T001
#      |--- DNS_2023-02-14.xlsx
#      |--- IPS_2023-02-14.xlsx
#      |--- WEB_2023-02-14.xlsx
# |--- T002
#      |--- DNS_2023-02-14.xlsx
#      |--- IPS_2023-02-14.xlsx
#      |--- WEB_2023-02-14.xlsx
#
# === crontab -e example===
# To create a cron job that executes a script every 15 minutes between 12:00am to 6:00am:
#
# */15 0-5 * * * /usr/bin/python3 /home/col/projects/python/py-unzip/unzip_script.py /home/col/projects/root
#
# */15: Run the command every 15 minutes
# 0-5: Run the command for hours between 0 (midnight) and 5 (5:59am)
#  *: Run the command every day of the month
#  *: Run the command every month
#  *: Run the command every day of the week

#################################################
# code for logging
#################################################
# Import Logging
import logging
logger = logging.getLogger("unzip_script")
logger.setLevel(logging.DEBUG)

DATE = datetime.now().strftime("%Y%m%d")
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create Handlers(Filehandler with filename| StramHandler with stdout)
file_handler_info = logging.FileHandler(os.path.join(script_dir, 'log', 'unzip_script_info_'+ DATE +'.log'))
# file_handler_debug = logging.FileHandler(os.path.join(script_dir, 'log', 'unzip_script_debug_'+DATE+'.log'))
stream_handler = logging.StreamHandler(sys.stdout)

# Set Additional log level in Handlers if needed
file_handler_info.setLevel(logging.INFO)
# file_handler_debug.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.WARNING)

# Create Formatter and Associate with Handlers
tz = time.strftime('%z')

formatter = logging.Formatter(
    '%(asctime)s ' + tz + ' - %(name)s - %(levelname)s - %(message)s')
file_handler_info.setFormatter(formatter)
# file_handler_debug.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add Handlers to logger
logger.addHandler(file_handler_info)
# logger.addHandler(file_handler_debug)
logger.addHandler(stream_handler)

#################################################
# code for unzip and rename script
#################################################

def unzip_n_delete(dir):
    # Function to unzip and del the zip

    os.chdir(dir) # change directory from working dir to dir with files
    print(f'### Script to unzip and delete zip in dir: {dir}')
    logger.info(f'### Script to unzip and delete zip in dir: {dir}')
    try:
        for f in os.listdir(dir): # loop through items in dir
            pattern = r"^(.*?)-\d{4}-\d{2}-\d{2}-\d{4}_\d{4}\.zip"
            print(f'processing file: {f}')
            logger.debug(f'processing file: {f}')

            if re.match(pattern, f):
                print(f' unzip file: {f}')
                logger.info(f' unzip file: {f}')

                fpath = os.path.abspath(f) # get full path
                zip_ref = zipfile.ZipFile(fpath) # create zipfile object
                zip_ref.extractall(dir) # extract
                zip_ref.close() # close
                os.remove(fpath) # delete zipped file
            else:
                print(f' Not match, skip: {f}')
                logger.info(f' Not match, skip: {f}')
    except Exception:
        pass
    return

def rename_csv(dir):
    # Function to remane csv
    
    os.chdir(dir) # change directory from working dir to dir with files
    print(f'### Script to rename csv in dir: {dir}')
    logger.info(f'### Script to rename csv in dir: {dir}')
    try:
        print(os.listdir(dir))
        for f in os.listdir(dir):
            pattern = r"^(.*?)-\d{4}-\d{2}-\d{2}-\d{4}_\d{4}\.csv"
            print(f'processing file: {f}')
            logger.debug(f'processing file: {f}')

            if re.match(pattern, f):
                # rename csv
                print(f' found match: {f}')
                logger.info(f' found match: {f}')
                fn = f.split("-") 
                # ['T001', 'IPS', '2023', '09', '22', '0000_6896.csv']
                #   f[0]    f[1]   f[2]   f[3]  f[4]
                f_newname_csv = fn[1]+'_'+fn[2]+'-'+fn[3]+'-'+fn[4]+'.csv'
                if os.path.exists(f_newname_csv) == True:
                    os.remove(f)
                    logger.info(f' found duplicate filename, deleted old file: {f_newname_csv}')
                print(f' rename to: {f_newname_csv}')
                logger.info(f' rename to: {f_newname_csv}')
                os.rename(f, f_newname_csv)

                # convent csv to xlsx
                convent_csv_xlsx(f_newname_csv)

            else:
                print(f' Not match, skip: {f}')
                logger.info(f' Not match, skip: {f}')

    except Exception:
        pass
    return


def convent_csv_xlsx(f_csv):
    # Function to convent csv to xlsx
    print(f'### Script to convent csv to xlsx: {f_csv}')
    logger.info(f'### Script to convent csv to xlsx: {f_csv}')

    f_xlsx = f_csv[:-4] + '.xlsx'

    try:
        df = pd.read_csv(f_csv)
    except pd.errors.EmptyDataError:
        print(f' Empty csv')
        logger.info(f' Empty csv')
        df = pd.DataFrame() #create a empty dataframe

    df.to_excel(f_xlsx, index=False)
    print(f' convent from csv to xlsx: {f_xlsx}')
    logger.info(f' convent from csv to xlsx: {f_xlsx}')
    return


def process_input_dir(dir):
    # child dir for processing, pattern is T001, T002, T003 ...etc
    pattern = r'T\d{3}'

    for f in os.listdir(dir):
        print('#'*50)
        print(f'###### START PROCESSING PATH: {dir}/{f}')
        logger.info(f'###### START PROCESSING PATH: {dir}/{f}')

        if re.match(pattern, f):
            print(f' found match: {f}')
            logger.info(f' found match: {f}')
            # unzip
            unzip_n_delete(os.path.join(dir, f))
            # rename and convent to csv
            rename_csv(os.path.join(dir, f))
        else:
            logger.info(f' Not match, skip: {f}')
            print(f' Not match, skip: {f}')
    return


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Fail to execute, Usage: python unzip_script.py <full_root_path_to_process>")
        logger.info(f'Fail to execute, Usage: python unzip_script.py <full_root_path_to_process>')
        sys.exit(1)
    dir = sys.argv[1]
    # dir = '/home/col/projects/python/py-unzip/report_dir'

    print(f'###')
    logger.info(f'###')
    print(f'###')
    logger.info(f'###')
    print(f'############### START SCRIPT TO SEARCH Txxx in: {dir} ############')
    logger.info(f'############ START SCRIPT TO SEARCH Txxx in: {dir} ############')

    process_input_dir(dir)

    print(f'############    END SCRIPT    ############ ')
    logger.info(f'############    END SCRIPT    ############ ')
