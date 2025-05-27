import requests
from datetime import datetime

API_KEY = "ur52Cn8VansiPR78cMZdHB9NdXh7OkwM"

def get_exchange_rate(to_currency='USD'):
    today = datetime.now().strftime("%Y%m%d")
    print("📅 요청 날짜:", today)

    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    params = {
        "authkey": API_KEY,
        "searchdate": today,
        "data": "AP01"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        print("📡 응답 코드:", response.status_code)
        data = response.json()
        for item in data:
            print("📄 통화 항목:", item["cur_unit"])
            if item["cur_unit"] == to_currency:
                print("✅ 매칭 성공:", item["deal_bas_r"])
                return float(item["deal_bas_r"].replace(",", ""))
    except Exception as e:
        print("❌ API 오류:", e)

    return None

# 테스트 실행
rate = get_exchange_rate("USD")
print("📣 받아온 환율 값:", rate)

if rate:
    print(f"✅ 오늘의 환율: 1 USD = {rate}원")
else:
    print("❌ 환율 정보를 가져올 수 없습니다.")