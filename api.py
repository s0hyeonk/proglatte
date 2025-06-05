import requests
from datetime import datetime
import certifi

API_KEY = "ur52Cn8VansiPR78cMZdHB9NdXh7OkwM"

def get_exchange_rate(to_currency='USD'):
    today = datetime.now().strftime("%Y%m%d")  
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

    params = {
        "authkey": API_KEY,
        "searchdate": today,
        "data": "AP01"
    }

    try:
        response = requests.get(url, params=params, timeout=5, verify=certifi.where())
        data = response.json()
        for item in data:
            if 'USD' in item["cur_unit"]:
                return float(item["deal_bas_r"].replace(",", ""))
    except:
        response = requests.get(url, params=params, timeout=5, verify=False)
        data = response.json()
        for item in data:
            if 'USD' in item["cur_unit"]:
                return float(item["deal_bas_r"].replace(",", ""))