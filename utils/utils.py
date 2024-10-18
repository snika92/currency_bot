import requests
import json
from dotenv import load_dotenv
import os
import datetime


load_dotenv()  # Загружает переменные

API_KEY = os.getenv('RATE_API_KEY')
CURRENCY_RATES_FILE = os.path.join("..", "src", "currency_rates.json")


def get_currency_rate(currency: str) -> float:
    """Запрашивает курс валюты от API и возвращает его в виде float"""
    # base = 'RUB' Внизу указываем, что искать нужно относительно рубля, поэтому здесь не нужно
    # url = "https://api.apilayer.com/exchangerates_data/latest?symbols=" + base + "&base=" + currency
    url = "https://api.apilayer.com/exchangerates_data/latest"
    # payload = {}
    headers = {
        "apikey": API_KEY
    }
    # params = {"symbols": base,
    #           "base": currency}
    params = {"base": currency}
    # response = requests.request("GET", url, headers=headers, data=payload)
    response = requests.get(url, headers=headers, params=params)
    print(response)

    result = json.loads(response.text)
    # result = response.json()['rates']['RUB']  #почему-то не работало
    return result['rates']['RUB']
    # print(result)


def save_to_json(currency, rate) -> None:
    """Сохраняет данные в JSON-файл"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {"Currency": currency,
            "Rate": rate,
            "Timestamp": timestamp}

    with open(CURRENCY_RATES_FILE, "a") as file:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], file)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, "w") as json_file:
                json.dump(data_list, json_file)




# print(get_currency_rate("EUR"))
# save_to_json({"Валюта": "USD", "Время": "10.29"})

#
# print(compare_to_previous_rate('USD', 97.159847))
# print(compare_to_previous_rate('USD', 97.150457))
# print(compare_to_previous_rate('EUR', 105.533512))
# print(compare_to_previous_rate('EUR', 105.12))
