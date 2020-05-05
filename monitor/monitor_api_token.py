import smtplib
import requests
import schedule
import time
import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

mail = EMAIL_ADDRESS
pwd = EMAIL_PASSWORD

api_dict = {"INSTITUTIONS": "http://iq-dev-api.fintuple.com/iq/institutions",
            "PROFESSIONALS": "https://iq-dev-api.fintuple.com/iq/professionals"}


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


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
            api_request = requests.get(v, auth=BearerAuth(
                'eyJraWQiOiJlZUM1UEN4dVBCeExPSHBuTmlQTlRyQzluNGFaOUdJUG8reHdKSTRKQUxFPSIsImFsZyI6IlJTMjU2In0.eyJzdWI'
                'iOiI5ODFmYmUxMy00NzNiLTRhZGQtOTU2YS03MmZjZmFkZTZhODYiLCJjb2duaXRvOmdyb3VwcyI6WyJmdHRlc3Rwb29sIl0sIm'
                'VtYWlsX3ZlcmlmaWVkIjp0cnVlLCJjb2duaXRvOnByZWZlcnJlZF9yb2xlIjoiYXJuOmF3czppYW06OjYwODE4NzE1ODA3Mzpyb'
                '2xlXC9hcC1zb3V0aC0xX09NTm5aQXBPUC1mdHRlc3Rwb29sR3JvdXBSb2xlIiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRw'
                'LmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV9PTU5uWkFwT1AiLCJjb2duaXRvOnVzZXJuYW1lIjoiOTgxZmJ'
                'lMTMtNDczYi00YWRkLTk1NmEtNzJmY2ZhZGU2YTg2IiwiY29nbml0bzpyb2xlcyI6WyJhcm46YXdzOmlhbTo6NjA4MTg3MTU4MD'
                'czOnJvbGVcL2FwLXNvdXRoLTFfT01OblpBcE9QLWZ0dGVzdHBvb2xHcm91cFJvbGUiXSwiYXVkIjoiN2FjZnJncnYzMzBibW5ma'
                '3U3N3RuNGk3YTgiLCJldmVudF9pZCI6ImVlYzEzZjMzLWVjZTItNDUzNy1hNWFjLTQ4ZDYyNjQ5MzZiNSIsInRva2VuX3VzZSI6'
                'ImlkIiwiYXV0aF90aW1lIjoxNTgyMDA3OTY0LCJleHAiOjE1ODIwMTE1NjcsImlhdCI6MTU4MjAwNzk2NywiZW1haWwiOiJqYWd'
                'hbkBmaW50dXBsZS5jb20ifQ.E9cHcy4sbo3HGDAjwIdAjlV5zrkj1o2dTVuW9ExFqMIoCzcC_xXv84Kkac4UFRyjTQi9Gl8QjAX'
                'aknBL-U95bV1Ac4fShsd34tsKU7ynKqmzPq6OSMEYvQQt6E3-3DPeeb4FbJ5gYCoephNMvEznvTjsM0QNkJryH39xQhO2CA2wmJ'
                '9uifDb32AAumlhIKTMyNUhiq_9JYAkfp0_kgXYSJDrp-Sf-8iKBLURPxNcWEEdaySPMza1MIkBdHvV0BXjJHc99b4TAnOf_5teE'
                'UlrEuZrt5Px907_8cTatuDAJWJRooQohRJI9zdaIhMn_oLIPhOdwmIzFzUIBZZsYLQZYA'))
            if api_request.status_code != 200:
                notify(api_request, k, v)
            else:
                print(datetime.datetime.now(), k,  ": working fine")
    except Exception as error:
        # notify(api_request, k, v)
        print("Exception occured", error)


schedule.every(1).minutes.do(api_notify)
while True:
    schedule.run_pending()
    time.sleep(1)
