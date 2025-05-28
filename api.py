import requests
from datetime import datetime
import certifi

API_KEY = "ur52Cn8VansiPR78cMZdHB9NdXh7OkwM"

def get_exchange_rate(to_currency='USD'):
    today = datetime.now().strftime("%Y%m%d")  
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    print("요청 날짜:", today)

    params = {
        "authkey": API_KEY,
        "searchdate": today,
        "data": "AP01"
    }
    headers = {
    "User-Agent": "Mozilla/5.0",
   }
    print("인증서 경로:", certifi.where())

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5, verify=False)
        data = response.json()
        for item in data:
            if 'USD' in item["cur_unit"]:
                return float(item["deal_bas_r"].replace(",", ""))
    except Exception as e:
        print("환율 API 실패:", e)
        return None
