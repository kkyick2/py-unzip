
import os

dir = '/home/col/projects/python/py-unzip_script/report_dir'
for f in os.listdir(dir):
    path = os.path.join(dir, f)
    print(path)
    print(os.path.isdir(path))
    item_in_dir = 0
    if(os.path.isdir(path)):
        item_in_dir = len(os.listdir(path))
    print(item_in_dir)