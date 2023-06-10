import requests
import json




api_key = "546fc8e5dd93bceaedc42572eee7749a"
cityname = "kassel"
url= f"http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit=5&appid={api_key}"

responce = requests.get(url)
data = responce.json()

result = {}

for item in data:
    result[item["name"]] = item 

lon = result["Kassel"]["lon"]
lat = result["Kassel"]["lat"]
