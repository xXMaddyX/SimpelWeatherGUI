import requests
import json



lang = "de"
api_key = "546fc8e5dd93bceaedc42572eee7749a"
url = f"http://api.openweathermap.org/data/2.5/weather?q=kassel,de&APPID={api_key}&lang={lang}"
response = requests.get(url)
data = json.loads(response.text)



#temp call
print(data["main"]["temp"])