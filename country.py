from config import base_url, auth_params
from model import Country
import glob
import os
import csv
import requests
import json


path = r'./csv' # use your path
all_files = glob.glob(os.path.join(path, "countries.csv"))


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']

headers = {"Authorization": "Bearer " + id_token}
response = requests.get(base_url + '/api/countries', headers=headers)


def get_country_by_name(country_name):
    response = requests.get(base_url + '/api/_search/countries', headers=headers, data={'query':country_name})
    if(response.status_code) != 500:
        response = response.json()
        if len(response) > 0 and response[0] is not None and response[0]['name'] == country_name:
            country = Country()
            country.id = response[0]['id']
            country.name = response[0]['name']
            country.isoCode = response[0]['isoCode']
            country.urduName = response[0]['urduName']
            country.addressUnitIdentifier = response[0]['addressUnitIdentifier']        
            return country


def import_countries():
    with open("./csv/countries.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_country_by_name(data[0].strip()) is None:
                country = {}
                country['name'] = data[0].strip()
                country['isoCode'] = data[1].strip()
                country['urduName'] = data[2].strip()
                country['addressUnitIdentifier'] = data[3].strip()
                response = requests.post(base_url + '/api/countries',headers=headers, json=country)








# for filename in all_files:
#     with open(filename, newline='') as csvfile:
#         csv_file = csv.reader(csvfile, delimiter=',', quotechar='"')
#         next(csv_file, None)
#         call_type = DimCallType()
#         deal = DimDeal()
#         disposition = DimDisposition()        
#         for row in csv_file:
#             call = FactCall()
#             try:                
#                 disposition = session.query(DimDisposition).filter(DimDisposition.disposition==row[11]).first()
#                 # Check if it is an incoming call
#                 if row[4] == 'from-queue-exten-internal':
#                 # if row[4] == 'none calls':
                    
                
            
    
    