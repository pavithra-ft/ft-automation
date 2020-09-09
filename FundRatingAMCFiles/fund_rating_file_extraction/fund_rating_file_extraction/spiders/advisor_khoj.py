import os
import scrapy
import zipfile
import requests
from ..settings import BASE_DIR


class AdvisorKhoj(scrapy.Spider):
    name = "advisor_khoj"
    allowed_domains = ['https://www.advisorkhoj.com']
    start_url = ["https://www.advisorkhoj.com/mutual-funds-research/mutual-fund-portfolio/"]

    def start_requests(self):
        year = "2020"
        amc_dict = {
            'ADITYABIRLA': 'Aditya-Birla-Sun-Life-Mutual-Fund',
            'BARODA': 'Baroda-Mutual-Fund',
            'BOI': 'BOI-AXA-Mutual-fund',
            'HDFC': 'HDFC-Mutual-Fund',
            'ICICI': 'ICICI-Prudential-Mutual-Fund',
            'IDBI': 'IDBI-Mutual-Fund',
            'KOTAK': 'Kotak-Asset-Management',
            'L&T': 'L&T-Mutual-Fund',
            'MAHINDRA': 'Mahindra-Mutual-Fund',
            'NIPPON': 'Nippon-India-Mutual-Fund',
            'PGIM': 'PGIM-India-Mutual-Fund',
            'SBI': 'SBI-Mutual-Fund',
            'SUNDARAM': 'Sundaram-Mutual-Fund'
        }
        for amc_key, amc_value in amc_dict.items():
            url = self.start_url[0] + amc_value + "/" + year
            yield scrapy.Request(url=url, callback=self.parser, meta={'amc_key': amc_key})

    def parser(self, response):
        link = {}
        link.update({response.meta.get('amc_key'): response.css('div[class="col-md-12 col-sm-12 '
                                                                'remove-bootstrap-col-lr-padding"] div p '
                                                                'a::attr(href)').getall()[0]})
        for amc, url_value in link.items():
            if 'kotak' not in url_value:
                download_format = url_value.split('/')[-1].split('.')[1]
                if len(download_format) > 3 or len(download_format) > 4:
                    download_format = download_format.split('?')[0]
                if download_format == 'zip':
                    save_zip(amc, url_value)
                elif download_format == 'xlsb' or download_format == 'xls' or download_format == 'xlsx':
                    save_xlsx(amc, url_value)
            else:
                save_xlsx(amc, url_value)


def save_zip(amc, url):
    data = requests.get(url)
    content = data.content
    zip_filename = BASE_DIR + "/fund_rating_file_extraction/zip_files/" + amc.lower() + '.zip'
    with open(zip_filename, 'wb') as f:
        f.write(content)
    extract_zip_files(zip_filename)


def save_xlsx(amc, url):
    data = requests.get(url)
    content = data.content
    filename = BASE_DIR + "/fund_rating_file_extraction/extracted_files/" + amc.lower() + '.xlsx'
    with open(filename, 'wb') as f:
        f.write(content)


def extract_zip_files(zip_filename):
    source_dir = BASE_DIR + "/fund_rating_file_extraction/zip_files"
    target_dir = BASE_DIR + "/fund_rating_file_extraction/extracted_files/"

    filelist = []
    with zipfile.ZipFile(zip_filename, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            filelist.append(elem.split('/')[-1])

    for item in os.listdir(source_dir):
        if item.endswith(".zip"):
            file_path = os.path.join(source_dir, item)
            with zipfile.ZipFile(file_path) as zf:
                if len(filelist) > 1:
                    for target_file in filelist:
                        if target_file in zf.namelist():
                            target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + '.xlsx'
                            target_path = os.path.join(target_dir, target_name)
                            with open(target_path, "wb") as f:
                                f.write(zf.read(target_file))
                else:
                    for target_file in filelist:
                        if target_file in zf.namelist():
                            target_name = item.split('.')[0] + '.xlsx'
                            target_path = os.path.join(target_dir, target_name)
                            with open(target_path, "wb") as f:
                                f.write(zf.read(target_file))
