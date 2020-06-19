import logging
import requests
from concurrent.futures import ThreadPoolExecutor


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class PDFServices:
    def generate_pdf(self, code, access_token):
        logging.basicConfig(filename="collateral_log.txt",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        URL = "https://dev-api.fintuple.in/fspdf/generate-pdf/{}"
        api_request = requests.post(url=URL.format(code), auth=BearerAuth(access_token))
        logger.info("CollateralCode : " + code + ", Status : " +
                    str(api_request.status_code))


def main(collateral_codes, access_token):
    pdf = PDFServices()
    executor = ThreadPoolExecutor(max_workers=1)
    for code in collateral_codes:
        task1 = executor.submit(pdf.generate_pdf, code, access_token)


collateral_codes = []

access_token = ''

if __name__ == '__main__':
    main(collateral_codes, access_token)
