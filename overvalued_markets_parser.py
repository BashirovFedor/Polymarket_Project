import requests
import json
url = "https://gamma-api.polymarket.com/events"

params = {
    "limit": 100,
    "active": True,
    "closed": False,
    "negRisk": True,
    "order": "liquidity",
    "ascending": False,
    "offset": 0
}

enough_liquidity = True
while enough_liquidity:
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Ошибка! {response.status_code}: {response.text}")
        break

    else:
        data = response.json()

        if not data:
            break

        for event in data:
            if (event.get("liquidity") or 0) < 1000:
                enough_liquidity = False
                break

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

                if (market.get("liquidityNum") or 0) < 1000:
                    break

                sum_yes += float(prices[0])
            else:
                if sum_yes > 1:
                    print(f"https://polymarket.com/event/{event["slug"]} | Сумма Yes: {sum_yes:.4f}")
    
    params["offset"] += 100