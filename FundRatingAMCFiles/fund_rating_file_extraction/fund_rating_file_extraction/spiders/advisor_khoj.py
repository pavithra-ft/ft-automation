import os
import scrapy
import zipfile
import requests
from ..config.urls import *
from ..config.file_extensions import *
from ..config.amc_dictionary import amc_dict
from ..config.web_elements import advisor_khoj_path
from ..config.selenium_chrome import EXTRACTED_DIR, ZIP_DIR, YEAR


class AdvisorKhoj(scrapy.Spider):
    name = "advisor_khoj_crawler"
    allowed_domains = [allowed_domains[0]]
    start_url = [start_url[0]]

    def start_requests(self):
        """
        This function loops through all the AMC's in the given dictionary with the Query parameters of the URL.
        With the built up URL, the Scrapy Request will be sent.
        """
        for amc_key, amc_value in amc_dict.items():
            url = self.start_url[0] + amc_value + "/" + str(YEAR)
            yield scrapy.Request(url=url, callback=self.parser, meta={'amc_key': amc_key})

    def parser(self, response):
        """
        This function gets the Response from the given URL and passes the response to the specific download formats.

        :param response: Response received from the URL.
        """
        link = {}
        link.update({response.meta.get('amc_key'): response.css(advisor_khoj_path[0]).getall()[0]})

        for amc, url_value in link.items():
            if 'kotak' not in url_value:
                download_format = url_value.split('/')[-1].split('.')[1]
                if len(download_format) > 3 or len(download_format) > 4:
                    download_format = download_format.split('?')[0]
                if download_format == zip_format:
                    save_zip(amc, url_value)
                elif download_format == xlsb_format or download_format == xls_format or download_format == xlsx_format:
                    save_xlsx(amc, url_value)
            else:
                save_xlsx(amc, url_value)


def save_zip(amc, url):
    """
    This function saves the downloaded Zip files.

    :param amc: Name of the AMC
    :param url: URL of the AMC
    """
    data = requests.get(url)
    content = data.content
    zip_filename = ZIP_DIR + '/' + amc.lower() + zip_ext
    with open(zip_filename, 'wb') as f:
        f.write(content)
    extract_zip_files(amc, zip_filename)


def save_xlsx(amc, url):
    """
    This function saves the downloaded XLSX files.

    :param amc: Name of the AMC
    :param url: URL of the AMC
    """
    data = requests.get(url)
    content = data.content
    filename = EXTRACTED_DIR + '/' + amc.lower() + xlsx_ext
    with open(filename, 'wb') as f:
        f.write(content)


def extract_zip_files(amc, zip_filename):
    """
    This function extracts the files inside the Zip files and saves it as an XLSX file.

    :param amc: Name of the AMC
    :param zip_filename: Name of the Zip file
    """
    filelist = []
    with zipfile.ZipFile(zip_filename, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            filelist.append(elem.split('/')[-1])

    for item in os.listdir(ZIP_DIR):
        if item.endswith(zip_ext):
            file_path = os.path.join(ZIP_DIR, item)
            with zipfile.ZipFile(file_path) as zf:
                if len(filelist) > 1:
                    for target_file in filelist:
                        if target_file in zf.namelist():
                            if amc == 'ICICI' and target_file == 'Debt' + xlsx_ext:
                                target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + xlsx_ext
                                target_path = os.path.join(EXTRACTED_DIR, target_name)
                                with open(target_path, "wb") as f:
                                    f.write(zf.read(target_file))
                            elif amc != 'ICICI':
                                target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + xlsx_ext
                                target_path = os.path.join(EXTRACTED_DIR, target_name)
                                with open(target_path, "wb") as f:
                                    f.write(zf.read(target_file))
                else:
                    for target_file in filelist:
                        if target_file in zf.namelist():
                            target_name = item.split('.')[0] + xlsx_ext
                            target_path = os.path.join(EXTRACTED_DIR, target_name)
                            with open(target_path, "wb") as f:
                                f.write(zf.read(target_file))
