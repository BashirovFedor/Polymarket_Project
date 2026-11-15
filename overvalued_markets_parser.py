import requests
import json
url = "https://gamma-api.polymarket.com/events"

params = {
    "limit": 50,
    "active": True,
    "closed": False,
    "negRisk": True
}
response = requests.get(url, params=params)

if response.status_code != 200:
    print(f"Ошибка! {response.status_code}: {response.text}")

else:
    data = response.json()

    for event in data:
        sum_yes = 0

        for market in event["markets"]:
            if any([not market.get("acceptingOrders"), market.get("umaResolutionStatus"), not market.get("negRisk")]):
                continue

            raw_prices = market.get("outcomePrices")
            if not raw_prices:
                continue

            prices = json.loads(raw_prices)
            if not prices:
                continue

            sum_yes += float(prices[0])

        if sum_yes > 1:
            print(f"https://polymarket.com/event/{event["slug"]} | Сумма Yes: {sum_yes:.4f}")