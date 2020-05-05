import logging
import requests


api_list = ["https://dev-api.fintuple.com/fspdf/generate-pdf/49249840",
            "https://dev-api.fintuple.com/fspdf/generate-pdf/55866782"]

access_token = 'jhfsdsjsddcsdnfbkeejeheddguwyhsdcmdcusdfhdsmcsdcahsdjfadshjasbk'


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def api_notify():
    global logger
    try:
        logging.basicConfig(filename="collateral_log.txt",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        for url in api_list:
            api_request = requests.get(url, auth=BearerAuth(access_token))
            if api_request.status_code != 200:
                logger.info("URL : " + url + ", Status : " + str(api_request.status_code))
            else:
                logger.info("URL : " + url + ", Status : " + str(api_request.status_code))
    except Exception as error:
        logger.info("Exception : " + str(error))


api_notify()
