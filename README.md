# py-unzip
kkyick2, 20230707, for hkstp use

# How to use

method1: Usage: python unzip_script.py <full_root_path_to_process>

```sh
col@ub22201:~/projects/python/py-unzip$ python3 unzip_script.py /home/col/projects/python/py-unzip/report_dir
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
*/15 0-5 * * * /usr/bin/python3 /home/col/projects/python/py-unzip/unzip_script.py /home/col/projects/root

*/15: Run the command every 15 minutes
0-5: Run the command for hours between 0 (midnight) and 5 (5:59am)
 *: Run the command every day of the month
 *: Run the command every month
 *: Run the command every day of the week
 ```