import scrapy

from scrapy_splash import SplashRequest
from ..items import BseSectorItem


class BseSector(scrapy.Spider):
    name = "bse_sector"
    allowed_domains = ["https://www.bseindia.com"]
    start_url = "https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=BSE30&index_Code=16"

    def start_requests(self):
        bse_sector_dict = {
            'BSE100': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=BSE100&index_Code=22',
            'BSE200': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=BSE200&index_Code=23',
            'BSE500': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=BSE500&index_Code=17',
            'BSEMC': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=MIDCAP&index_Code=81',
            'BSEMSC400': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=MSL400&index_Code=105',
            'BSESC': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=SMLCAP&index_Code=82',
            'SENSEX': 'https://www.bseindia.com/sensex/IndicesWatch_Sector.aspx?iname=BSE30&index_Code=16'}

        for index_code, sector_url in bse_sector_dict.items():
            yield SplashRequest(url=sector_url, callback=self.sector_parser, meta={'index_code': index_code})

    def sector_parser(self, response):
        table = response.css('div[class="col-lg-12 largetable"] table tbody tr td table tbody tr td')[0]
        for index, row in enumerate(table.css('table > tbody > tr')):
            if index == 3:
                items = BseSectorItem()
                items['index_code'] = response.meta.get('index_code')
                items['sector_name'] = row.css('td:nth-child(2)::text').extract_first()
                items['sector_exposure'] = row.css('td:nth-child(3)::text').extract_first()
                yield items
