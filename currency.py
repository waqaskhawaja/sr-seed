from config import base_url, auth_params
from model import Currency
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_currency_by_code(currency_code):
    local_response = requests.get(base_url + '/api/_search/currencies', headers=headers, data={'query': currency_code})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None and local_response[0]['code'] == currency_code:
            currency = Currency()
            currency.id = local_response[0]['id']
            currency.name = local_response[0]['name']
            currency.urduName = local_response[0]['urduName']
            currency.code = local_response[0]['code']
            return currency


def import_currencies():
    with open("./csv/currencies.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:                        
            if get_currency_by_code(data["code"].strip()) is None:
                gender = {'name': data["name"].strip(), 'code': data["code"].strip()}
                requests.post(base_url + '/api/currencies', headers=headers, json=gender)



