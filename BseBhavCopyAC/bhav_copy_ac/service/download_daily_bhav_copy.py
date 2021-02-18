import os
import zipfile
import requests
from bhav_copy_ac.config.bhav_copy_config import *


def download_file(bse_bhav_copy_url):
    download_url = bse_bhav_copy_url + recent_working_day + file_extensions[0]
    request_headers = requests.head(download_url)
    data = requests.get(download_url, stream=True, headers=request_headers)
    content = data.content
    zip_filename = zip_file_dir[0] + "/" + zip_file_name[0] + file_extensions[0]
    with open(zip_filename, 'wb') as f:
        f.write(content)
    return zip_filename


def extract_zip_files(zip_filename):
    filelist = []
    with zipfile.ZipFile(zip_filename, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            filelist.append(elem.split('/')[-1])

    for item in os.listdir(zip_file_dir[0]):
        if item.endswith(file_extensions[0]):
            file_path = os.path.join(zip_file_dir[0], item)
            with zipfile.ZipFile(file_path) as zf:
                for target_file in filelist:
                    if target_file in zf.namelist():
                        target_name = csv_file_name[0] + file_extensions[1]
                        target_path = os.path.join(csv_file_dir[0], target_name)
                        with open(target_path, "wb") as f:
                            f.write(zf.read(target_file))
