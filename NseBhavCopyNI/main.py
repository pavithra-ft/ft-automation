import requests

get_url = "https://ni-dev-api.fintuple.in/onboarding/ni/bhavCopyData/INE006I01046"

# request_headers = requests.head(get_url)
data = requests.get(get_url, stream=True)
print(data.json())
