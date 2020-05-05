import smtplib
import requests
import schedule
import time
import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

mail = EMAIL_ADDRESS
pwd = EMAIL_PASSWORD

site_dict = {"FINTUPLE": "https://fintuple.com",
             "FINTUPLE - IQ": "https://iq-dev.fintuple.com/",
             }


def notify(site_request, k, v):
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "SITE IS DOWN!"
        body = k + " - Site is down"
        if site_request.status_code == 525:
            code = "Captured code : " + str(site_request.status_code)
            code_content = "Error 525 indicates that the SSL handshake between Cloudflare and the origin web server " \
                           "failed. This only occurs when the domain is using Cloudflare Full or Full (Strict) SSL " \
                           "mode. This is typically caused by a configuration issue in the origin web server, " \
                           "when this happens, you’ll see “Error 525: SSL handshake failed” "
        elif site_request.status_code == 521:
            code = "Captured code : " + str(site_request.status_code)
            code_content = "A 521 error happens when we are unable to make a TCP connection to your origin server. " \
                           "Specifically, Cloudflare tried to connect to your origin server on port 80 or 443, " \
                           "but received a connection refused error. This is often caused by security or firewall " \
                           "software and happens if the origin server has directly refused Cloudflare’s proxy request. "
        elif site_request.status_code == 522:
            code = "Captured code : " + str(site_request.status_code)
            code_content = "Code 522 stands for 'Connection timed out', which occurs whenever the TCP handshake " \
                           "between the web server and Cloudflare fails. "
        else:
            code = "Captured code : " + str(site_request.status_code)
            code_content = ""
        url = "For your reference, URL : " + v
        msg = f'Subject: {subject}\n\n{body}\n{code}\n\n{code_content}\n\n{url}'
        smtp.sendmail(['notifications@fintuple.com'], ['pavithra@fintuple.com'], msg.encode("utf-8"))
        print(datetime.datetime.now(), k + ": mail sent")


def site_notify():
    try:
        for k, v in site_dict.items():
            site_request = requests.get(v, timeout=30)
            if site_request.status_code != 200:
                notify(site_request, k, v)
            else:
                print(datetime.datetime.now(), k, ": working fine")
    except Exception as error:
        notify(site_request)
        print("Exception occured :", error)


schedule.every(1).hours.do(site_notify)
while True:
    schedule.run_pending()
    time.sleep(1)
