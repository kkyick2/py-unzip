import sys,os,re,zipfile,time,csv
from datetime import datetime
from openpyxl import Workbook
import pandas as pd
import logging
version = '20240202'
# kkyick2, for hkstp
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
# global var
#################################################
DATE = datetime.now().strftime("%Y%m%d")
LOG_FILE_LEVEL = logging.INFO # set log file level
LOG_CONSOLE_LEVEL = logging.WARNING # set log console level
LOG_LOWEST_LEVEL = logging.DEBUG # set lowest log level
#################################################
# code for logging
#################################################
# Import Logging
logger = logging.getLogger("unzip_script")
logger.setLevel(LOG_LOWEST_LEVEL) # define the lowest-severity log message a logger will handle
script_dir = os.path.dirname(os.path.realpath(__file__))
# Create Handlers(Filehandler with filename| StramHandler with stdout)
file_handler = logging.FileHandler(os.path.join(script_dir, 'log', 'unzip_script_' + DATE + '.log'))
stream_handler = logging.StreamHandler(sys.stdout)
# Set Additional log level in Handlers if needed
file_handler.setLevel(LOG_FILE_LEVEL)
stream_handler.setLevel(LOG_CONSOLE_LEVEL)
# Create Formatter and Associate with Handlers
tz = time.strftime('%z')
formatter = logging.Formatter(
    '%(asctime)s ' + tz + ': %(name)s: %(process)d.%(thread)d: %(funcName)-18s: %(levelname)-8s: %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add Handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#################################################
# code for unzip and rename script
#################################################

def unzip_n_delete(dir):
    # Function to unzip and del the zip

    os.chdir(dir) # change directory from working dir to dir with files
    print(f'### Step1 - Script to unzip and delete zip in dir: {dir}')
    logger.info(f'### Step1 - Script to unzip and delete zip in dir: {dir}')
    if len(os.listdir(dir)) == 0:
        print(f' Empty dir, skip')
        logger.info(f' Empty dir, skip')
    else:
        try:
            for f in os.listdir(dir): # loop through items in dir
                pattern = r"^(.*?)-\d{4}-\d{2}-\d{2}-\d*_\d*\.zip"
                print(f' processing file: {f}')
                logger.debug(f' processing file: {f}')

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
    print(f'### Step2 - Script to rename csv in dir: {dir}')
    logger.info(f'### Step2 - Script to rename csv in dir: {dir}')
    if len(os.listdir(dir)) == 0:
        print(f' Empty dir, skip:')
        logger.info(f' Empty dir, skip:')
    else:
        try:
            for f in os.listdir(dir):
                pattern = r"^(.*?)-\d{4}-\d{2}-\d{2}-\d*_\d*\.csv"
                print(f' Processing file: {f}')
                logger.debug(f' Processing file: {f}')

                if re.match(pattern, f):
                    # rename csv
                    print(f' Found match: {f}')
                    logger.info(f' Found match: {f}')
                    fn = f.split("-") 
                    # ['T001', 'IPS', '2023', '09', '22', '0000_6896.csv']
                    #   f[0]    f[1]   f[2]   f[3]  f[4]
                    f_newname_csv = fn[1]+'_'+fn[2]+'-'+fn[3]+'-'+fn[4]+'.csv'
                    f_newname_xlsx = fn[1]+'_'+fn[2]+'-'+fn[3]+'-'+fn[4]+'.xlsx'
                    if os.path.exists(f_newname_csv) == True:
                        os.remove(f)
                        logger.info(f' Found duplicate filename, deleted old file: {f_newname_csv}')
                    print(f' Rename to: {f_newname_csv}')
                    logger.info(f' Rename to: {f_newname_csv}')
                    os.rename(f, f_newname_csv)

                    
                    print(f'### step2.0: checking {f_newname_csv} is empty csv?')
                    logger.info(f'### step2.0: checking {f_newname_csv} is empty csv?')
                    # step2A: if csv empty, create empty excel
                    if os.stat(f_newname_csv).st_size == 0:  
                        print(f' Empty csv, create empty xlsx')
                        logger.info(f' Empty csv, create empty xlsx')
                        df = pd.DataFrame() #create a empty dataframe
                        df.to_excel(f_newname_xlsx, index=False)

                        print(f' Delete old csv file: {f_newname_csv}')
                        logger.info(f' Delete old csv file: {f_newname_csv}')
                        os.remove(f_newname_csv)
                    # step2B: if csv not empty
                    else:
                        print(f' Not empty csv, process next step')
                        logger.info(f' Not empty csv, process next step')
                        # step2B1: handle web report with "0 " or "-nan" cell
                        if fn[1] == 'WEB':
                            modify_web_csv(f_newname_csv)
                        # step2B2: convent non empty csv to xlsx
                        convent_csv_xlsx(f_newname_csv)
                    
                else:
                    print(f' Not match, skip: {f}')
                    logger.info(f' Not match, skip: {f}')
        except Exception:
            print(f' Error exception: {Exception}')
            logger.info(f' Error exception: {Exception}')
            pass
    return

def modify_web_csv(f_csv):
    # Function to modify web report csv
    # fix middleware java program handle csv with error when cell have value "0 " and "-nan "
    # Example of first 4 rows of web report
    #
    #"###Total Requests###"
    #"Type","Requests","% of Total"
    #"Allowed","0 ","-nan "
    #"Blocked","0 ","-nan "
    #
    print(f'### Step2B1 - Script to modify web report csv: {f_csv}')
    logger.info(f'### Step2B1 - Script to modify web report csv: {f_csv}')

    fn = f_csv.split(".")
    f_csv_a = fn[0] + 'a.csv'

    # modify the web report csv
    with open(f_csv, "r") as inf:
        reader = csv.reader(inf)
        rows = list(reader)
        pattern1 = ['###Total Requests###']
        pattern2 = ['Allowed','Blocked']

        # row0 if match "###Total Requests###"
        if(rows[0][0] in pattern1):
            print(f' Reading row0 matched pattern1: {rows[0]}')
            logger.info(f' Reading row0 matched pattern1: {rows[0]}')
        
            # row2 "Allowed","0 ","-nan "
            print(f' Reading row2: {rows[2]}')
            logger.info(f' Reading row2: {rows[2]}')
            if(rows[2][0] in pattern2):
                rows[2][1] = rows[2][1].strip() # "0 " to "0"
                if(rows[2][2] == '-nan '):
                    rows[2][2] = '0'
            print(f' Edited row2: {rows[2]}')
            logger.info(f' Edited row2: {rows[2]}')

            # row3 "Blocked","0 ","-nan "
            print(f' Reading row3: {rows[3]}')
            logger.info(f' Reading row3: {rows[3]}')
            if(rows[3][0] in pattern2):
                rows[3][1] = rows[3][1].strip()
                if(rows[3][2] == '-nan '):
                    rows[3][2] = '0'
            print(f' Edited row3: {rows[3]}')
            logger.info(f' Edited row3: {rows[3]}')

            # Write new csv file
            with open(f_csv_a, "w", newline="") as outf:
                writer = csv.writer(outf)
                writer.writerows(rows)

            # WEB_2023-09-27.csv   <-- old, del this file
            # WEB_2023-09-27a.csv  <-- new, rename to WEB_2023-09-27.csv
            if os.path.exists(f_csv) == True:
                print(f' Delete old csv file: {f_csv}')
                logger.info(f' Delete old csv file: {f_csv}')
                os.remove(f_csv)
                print(f' Rename new csv {f_csv_a} to: {f_csv}')
                logger.info(f' Rename new csv {f_csv_a} to: {f_csv}')
                os.rename(f_csv_a, f_csv)
        # row0 if NOT match "###Total Requests###", skip
        else:
            print(f' skip when reading row0 NOT matched pattern1: {rows[0]}')
            logger.info(f' skip when reading row0 NOT matched pattern1: {rows[0]}')            

    return


def convent_csv_xlsx(f_csv):
    # Function to convent csv to xlsx
    print(f'### Step2B2 - Script to convent non empty csv to xlsx: {f_csv}')
    logger.info(f'### Step2B2 - Script to convent non empty csv to xlsx: {f_csv}')


    try:
        f_xlsx = f_csv[:-4] + '.xlsx'
        wb = Workbook()
        ws = wb.active
        with open(f_csv, 'r') as f:
            for row in csv.reader(f):
                ws.append(row)
        wb.save(f_xlsx)
        print(f' Convent from csv to xlsx: {f_xlsx}')
        logger.info(f' Convent from csv to xlsx: {f_xlsx}')
    except Exception:
        print(f' Error exception: {Exception}')
        logger.info(f' Error exception: {Exception}')
        pass
    # remove csv after convent to xlsx
    if(os.path.isfile(f_xlsx)):
        print(f' Found xlsx {f_xlsx} and remove csv')
        logger.info(f' Found xlsx {f_xlsx} and remove csv')
        os.remove(f_csv) 
    else:
        print(f' Convent fail!!! xlsx file not found!!!')
        logger.warning(f' Convent fail!!! xlsx file not found!!!')
    return


def process_input_dir(dir):
    # child dir for processing, pattern is T001, T002, T003 ...etc
    pattern = r'T\d{3}'

    for f in os.listdir(dir):
        print('#'*50)
        print(f'###### Step0 - START PROCESSING PATH: {dir}/{f}')
        logger.info('#'*50)
        logger.info(f'###### Step0 - START PROCESSING PATH: {dir}/{f}')

        if re.match(pattern, f):
            print(f' Found match: {f}')
            logger.info(f' Found match: {f}')

            # step1: unzip and delete
            unzip_n_delete(os.path.join(dir, f))

            # step2: rename and convent to xlsx, del csv afterward
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
    print(f'###')
    logger.info(f'###')
    logger.info(f'###')
    print(f'############################################################## ')
    print(f'##################       START SCRIPT       ################## ')
    print(f'### Search FAZ report csv in each folder, pattern is Txx in directory: {dir}')
    logger.info(f'############################################################## ')
    logger.info(f'##################       START SCRIPT       ################## ')
    logger.info(f'### Search FAZ report csv in each folder, pattern is Txx in directory: {dir}')

    process_input_dir(dir)

    print(f'###############       END SCRIPT       ############### ')
    print(f'###################################################### ')
    logger.info(f'###############       END SCRIPT       ############### ')
    logger.info(f'###################################################### ')