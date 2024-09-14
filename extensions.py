import requests
import json
from config import currencies, API_KEY

class APIException(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f"Вы ввели одинаковую валюту - {base}")
        
        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту - {base}")
        
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту - {quote}")
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество - {amount}")
        
        r = requests.get(f"https://apilayer.net/api/live?access_key={API_KEY}&currencies={quote_ticker}&source={base_ticker}&format=1")
        total_base = json.loads(r.content)["quotes"][currencies[base] + currencies[quote]] * amount
        
        return total_base