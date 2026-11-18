import requests
import json
from datetime import datetime, timezone, timedelta

url = "https://gamma-api.polymarket.com/events"
max_date = (datetime.now(timezone.utc) + timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")

params = {
    "limit": 100,
    "active": True,
    "closed": False,
    "negRisk": True,
    "order": "liquidity",
    "ascending": False,
    "exclude_tag_id": 1,
    "end_date_max": max_date,
    "offset": 0
}

event_list = []
enough_liquidity = True
while enough_liquidity and params["offset"] <= 1000:
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

            if not event.get("endDate"):
                continue

            sum_no = 0
            valid_market_number = 0
            for market in event["markets"]:
                
                if any([not market.get("acceptingOrders"), market.get("umaResolutionStatus"), not market.get("negRisk")]):
                    continue

                raw_prices = market.get("outcomePrices")
                if not raw_prices:
                    continue

                prices = json.loads(raw_prices)
                if not prices:
                    continue

                if any(
                    [(market.get("liquidityNum") or 0) < 1000,
                    (market.get("spread") or 1)  > 0.03,
                    (market.get("bestBid") or 0) < 0.001]
                ):
                    break

                sum_no += 1 - market["bestBid"]
                valid_market_number += 1
            else:
                if sum_no < valid_market_number - 1:
                    profit = (valid_market_number - 1 - sum_no) / sum_no * 100
                    apr = profit / ((datetime.fromisoformat(event["endDate"]) - datetime.now(timezone.utc)).total_seconds() / 86400) * 365
                    if apr >= 20:
                        event_list.append([event["slug"], apr])
    params["offset"] += 100

event_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
print(*(f"https://polymarket.com/event/{slug} | APR: {apr:.2f}%" for slug, apr in event_list), sep='\n')