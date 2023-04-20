import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod # статический метод получения
    def get_price(base, target, amount): # цен по исходной валюте (base), валюте перевода (target) и количеству валюты для перевода (amount)
        try:
            base_code = exchanges[base.lower()] #  проверка написания наименования нижним регистром
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            target_code = exchanges[target.lower()]
        except KeyError:
            raise APIException(f"Валюта {target} не найдена!")

        if base_code == target_code: # предупреждение о невозможности конвертации одинаковых валют
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount) # валюта задается числом с плавающей точкой
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        # запрос к API для получения обновленного списка валют конвертации
        r = requests.get(f"https://v6.exchangerate-api.com/v6/ed590f054301f5d8a96935cd/pair/{base_code}/{target_code}")
        resp = json.loads(r.content) # парсинг соотвeтствующего контента с API
        new_price = resp['conversion_rate'] * float(amount)
        new_price = round(new_price, 2) # ограничение количества знаком после точки
        message = f"{amount} {base_code} - {new_price} {target_code}"
        return message