import requests
import scrapy
from ..settings import BASE_DIR


class NsePdfSpider(scrapy.Spider):
    name = "nsepdfdownloader"
    allowed_domains = ['https://www1.nseindia.com']
    start_url = "https://www1.nseindia.com/products/content/equities/indices/broad_indices.htm"

    def start_requests(self):
        """
        This function loops through the indices and downloads the PDF of the corresponding index.
        """
        urls = {"NIFTY100": "https://www1.nseindia.com/products/content/equities/indices/nifty_100.htm",
                "NIFTY200": "https://www1.nseindia.com/products/content/equities/indices/nifty_200.htm",
                "NIFTY50": "https://www1.nseindia.com/products/content/equities/indices/nifty_50.htm",
                "NIFTY500": "https://www1.nseindia.com/products/content/equities/indices/nifty_500.htm",
                "NIFTYMC100": "https://www1.nseindia.com/products/content/equities/indices/nifty_midcap_100.htm",
                "NIFTYMC150": "https://www1.nseindia.com/products/content/equities/indices/nifty_midcap_150.htm",
                "NIFTYSC100": "https://www1.nseindia.com/products/content/equities/indices/nifty_smallcap_100.htm",
                "NIFTYSC250": "https://www1.nseindia.com/products/content/equities/indices/nifty_Smallcap_250.htm",
                "NIFTYPHARMA": "https://www1.nseindia.com/products/content/equities/indices/sectoral_indices.htm"
                }
        for index_code, url in urls.items():
            yield scrapy.Request(url=url, callback=self.pdf_parser, meta={'index_code': index_code})

    def pdf_parser(self, response):
        """
        This function downloads the PDF of the indices.

        :param response: Response from the URL
        """
        link = []
        index_code = response.meta.get('index_code')
        if index_code != "NIFTYPHARMA":
            pdf_urls = response.css('div[class="abt_equities_content"] p a::attr(href)').getall()[-1]
            link.append(self.allowed_domains[0] + pdf_urls)
        else:
            pdf_urls = response.css('div[class="abt_equities_content"] p a::attr(href)').getall()
            for pdf in pdf_urls:
                name = pdf.split('/')[-1]
                if name == "ind_nifty_pharma.pdf":
                    link.append(self.allowed_domains[0] + pdf)
        for pdf in link:
            self.save_pdf(pdf)

    def save_pdf(self, pdf):
        """
        This function saves the downloaded PDF in the given directory.

        :param pdf: Downloaded PDF
        """
        data = requests.get(pdf)
        content = data.content
        filename = BASE_DIR + "/extracted_pdf_files/" + pdf.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(content)
