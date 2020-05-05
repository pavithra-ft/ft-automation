import smtplib
import requests
import schedule
import time
import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

mail = EMAIL_ADDRESS
pwd = EMAIL_PASSWORD

api_dict = {"INSTITUTIONS": "http://13.234.239.228:8080/iq/institutions",
            "PROFESSIONALS": "http://13.234.239.228:8080/iq/professionals"}


def notify(api_request, k, v):
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "API IS DOWN!"
        body = k + ": API is down"
        code = "Captured code : " + str(api_request.status_code)
        url = "For your reference, URL : " + v
        msg = f'Subject: {subject}\n\n{body}\n{code}\n{url}'
        smtp.sendmail(['notifications@fintuple.com'], ['pavithra@fintuple.com'], msg)
        print(datetime.datetime.now(), k + " : mail sent")


def api_notify():
    try:
        for k, v in api_dict.items():
            api_request = requests.get(v)
            if api_request.status_code != 200:
                notify(api_request, k, v)
            else:
                print(datetime.datetime.now(), k,  ": working fine")
    except Exception as error:
        notify(api_request, k, v)
        print("Exception occured", error)


schedule.every(1).hours.do(api_notify)
while True:
    schedule.run_pending()
    time.sleep(1)
