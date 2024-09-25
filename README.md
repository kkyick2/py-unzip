# py-unzip_script
kkyick2, 20230707, for hkstp use

# How to use

method1: Usage: python unzip_script.py <full_root_path_to_process>

```sh
col@ub22201:~/projects/python/py-unzip_script$ python3 unzip_script_script.py /home/col/projects/python/py-unzip_script/report_dir
```


```sh
col@ub22201:~/projects/python/py-unzip_script$ source venv/bin/activate
(venv) col@ub22201:~/projects/python/py-unzip_script$
(venv) col@ub22201:~/projects/python/py-unzip_script$ python unzip_script.py /home/col/projects/python/py-unzip_script/report_dir
```

method2: create a cron job with 'crontab -e' and verify with 'crontab -l'


## Description

This script reead below folder structure, unzip pattern "xxxReport-YYYY-MM-DD-HHMM_SSSS.zip" and rename to "xxxReport-YYYY-MM-DD.csv"

Before:

```sh
report_dir
|--- T001
     |--- DNS Security Report-2023-02-14-1704_1915.zip
     |--- IPS Report-2023-02-14-1704_1915.zip
     |--- Web Usage Summary Report-2023-02-14-1704_1915.zip
|--- T002
     |--- DNS Security Report-2023-02-14-1704_1915.zip
     |--- IPS Report-2023-02-14-1704_1915.zip
     |--- Web Usage Summary Report-2023-02-14-1704_1915.zip
|--- T003
     |--- DNS Security Report-2023-02-14-1704_1915.zip
     |--- IPS Report-2023-02-14-1704_1915.zip
     |--- Web Usage Summary Report-2023-02-14-1704_1915.zip
```

After:

```
report_dir
|--- T001
     |--- DNS Security Report-2023-02-14.csv
     |--- IPS Report-2023-02-14-1704.csv
     |--- Web Usage Summary Report-2023-02-14.csv
|--- T002
     |--- DNS Security Report-2023-02-14.csv
     |--- IPS Report-2023-02-14-1704.csv
     |--- Web Usage Summary Report-2023-02-14.csv
|--- T003
     |--- DNS Security Report-2023-02-14.csv
     |--- IPS Report-2023-02-14-1704.csv
     |--- Web Usage Summary Report-2023-02-14.csv
```
## crontab -e example

To create a cron job that executes a script every 15 minutes between 12:00am to 6:00am:

```sh
*/15 0-5 * * * /usr/bin/python3 /home/col/projects/python/py-unzip_script/unzip_script.py /home/col/projects/root

*/15: Run the command every 15 minutes
0-5: Run the command for hours between 0 (midnight) and 5 (5:59am)
 *: Run the command every day of the month
 *: Run the command every month
 *: Run the command every day of the week
 ```

## History

| Version  | Date      | Description  |
| :------- | :-------- | :----------- |
| 20230707 | 2023-0707 | draft |
| 20231004 | 2023-1004 | use pandas to convent csv to xls |
| 20231012 | 2023-1012 | use xlswriter to convent csv to xls |
| 20240105 | 2024-0105 | use openpyxl to convent csv to xls |
| 20240122 | 2024-0122 | handle web report cell "-nan " and "0 " value |
| 20240202 | 2024-0202 | change filename pattern from (r"^(.*?)-\d{4}-\d{2}-\d{2}-\d{4}_\d{4}\.zip") to (r"^(.*?)-\d{4}-\d{2}-\d{2}-\d*_\d*\.zip")<br> fix empty csv cannot output xlsx issue |
| 20240926 | 2024-0926 | handle web report cell '-nan ' and "'-nan ", updated logging messages and with counter |