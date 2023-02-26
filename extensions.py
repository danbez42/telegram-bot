import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym_key} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base_key}!')

        try:
            amount = float(amount.replace(",","."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.request(\
            "GET", \
            f"https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}", \
            headers={"apikey": "1bo3Dr6iHfZitM150DKcYvpfnx6V2w3Z"}, \
            data={})
        resp_0 = json.loads(r.content)
        resp_1 = resp_0['rates']
        resp_2 = list(resp_1.values())
        resp = resp_2[0]
        new_price = round(float(resp) * float(amount), 2)

        message = f"По текущему курсу конвертация {amount} {base} в {sym} составляет: {new_price}"
        return message