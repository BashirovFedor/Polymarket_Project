import requests
import json
url = "https://gamma-api.polymarket.com/events"

params = {
    "limit": 3,
    "active": True,
    "closed": False,

}
response = requests.get(url, params=params)

if response.status_code != 200:
    print(f"Ошибка! {response.status_code}: {response.text}")
else:
    data = response.json()
    print("Ключи события:", json.dumps(list(data[0].keys()), indent=2))
    print()
    print("Ключи рынка:", json.dumps(list(data[0]["markets"][0].keys()), indent=2))