import requests

def get_exchange_rate(to_currency='USD'):
    url = f"https://api.exchangerate.host/latest?base=KRW&symbols={to_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        return data['rates'][to_currency]
    except:
        return None

def convert_currency(krw_amount, to_currency='USD'):
    rate = get_exchange_rate(to_currency)
    return round(krw_amount * rate, 2) if rate else None
