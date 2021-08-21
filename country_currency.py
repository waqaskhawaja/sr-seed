from config import base_url, auth_params
from model import Currency, Country
import country
import currency
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token, 'Connection': None, 'Accept-Encoding': None,
           'Content-type': 'application/json'}


def import_country_currency():
    with open("./csv/currency_to_country.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:            
            country_obj = country.get_country_by_iso_code(data["CountryCode"])
            currency_obj = currency.get_currency_by_code(data["Code"])
            if country_obj is not None and currency_obj is not None:
                country_obj.currency = currency_obj
                request_json: json = json.dumps(country_obj.__dict__, default=country_obj.encode_associations)
                requests.put(base_url + '/api/countries/' + str(country_obj.id),
                             headers=headers, data=request_json)
