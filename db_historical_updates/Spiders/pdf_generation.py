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
        # task3 = executor.submit(pdf.generate_pdf, collateral_codes, access_token)
        # task4 = executor.submit(pdf.generate_pdf, collateral_codes, access_token)
        # task5 = executor.submit(pdf.generate_pdf, collateral_codes, access_token)
        # task6 = executor.submit(pdf.generate_pdf, collateral_codes, access_token)


collateral_codes = ['62058038', '91521244', '33168729', '71516832', '39573033', '5107910', '77668511', '42996021',
                    '7457641', '35696347', '91466311', '89041459', '35216301', '77720341', '18831049', '92607444',
                    '62182152', '55751448', '87185395', '12010115', '2172458', '58519091', '50742717', '17633543',
                    '82113013', '93746535', '68917875', '63572921', '45944276', '18670067', '89644308', '10572925',
                    '81877496', '92657487', '45883387', '33567512', '59114332', '3648295', '83181214', '83382149',
                    '59317072']

access_token = 'eyJraWQiOiJlZUM1UEN4dVBCeExPSHBuTmlQTlRyQzluNGFaOUdJUG8reHdKSTRKQUxFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4ZjQ2MGJkMi1lZTZhLTQyZGYtODM3NS0wNmFiNzVhYTA0OTgiLCJhdWQiOiI3YWNmcmdydjMzMGJtbmZrdTc3dG40aTdhOCIsImV2ZW50X2lkIjoiYWY0Y2Q5MmQtYTEwNy00YjAzLWE5MzgtNjNjOTBjYzRiZWEwIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1ODc4MDI1NTcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoLTFfT01OblpBcE9QIiwiY29nbml0bzp1c2VybmFtZSI6IjhmNDYwYmQyLWVlNmEtNDJkZi04Mzc1LTA2YWI3NWFhMDQ5OCIsImV4cCI6MTU4NzgwNjE1NywiaWF0IjoxNTg3ODAyNTU3LCJlbWFpbCI6InJlc2VhcmNoQGZpbnR1cGxlLmNvbSJ9.lInhLAjDY5sptKJa-A2RIU5c5zFrsMOxMRMCX0mMcNar_yR4OKZ9QwWGvYW1hwH0wj1INbqLI1jFwtzdOl85Net-Hbv2H6RHJPrKa_R3T8JEHWQ7XjKIcGN-vYIG0KmPlkIEM1GPWErmCjbnPdCHlr4zfYiMtgzaJVgh98SI04Uf4ZdYosbeym88kSis34-0x6nl3nPxyC7cDPb9UCGfZxP3FCbL06PUImgp3yJ8fpSMkeKjD1zqUzVg7pSyURJ0neUYtfP9XywRhFQRqkGuDOs5ZvxT2n-6BKc43uQfJLPjdImJQw-Jo4itSyVVh2HiJ-a28CWswplg4ydqC1kpaQ'

if __name__ == '__main__':
    main(collateral_codes, access_token)
