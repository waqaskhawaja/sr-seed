from model import Country, CountryAdministrativeUnit
from datetime import datetime
import glob
import os
import csv
import sys
import requests
import json

base_url = 'http://localhost:9000'

path = r'./csv' # use your path
all_files = glob.glob(os.path.join(path, "countries.csv"))

auth_params = {'username':'admin','password':'admin'}
response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']

headers = {"Authorization": "Bearer " + id_token}
response = requests.get(base_url + '/api/countries', headers=headers)


def get_country_by_name(country_name):
    response = requests.get(base_url + '/api/_search/countries', headers=headers, data={'query':country_name})).text    
    if len(response) > 0 and response[0]['name'] == country_name:
        country = Country()
        country.id = response[0]['id']
        country.name = response[0]['name']
        country.iso_code = response[0]['isoCode']
        country.urdu_name = response[0]['urduName']
        country.address_unit_identifier = response[0]['addressUnitIdentifier']        
        return country


with open("./csv/countries.csv", encoding='utf-8') as files:
    reader = csv.reader(files)
    next(reader, None)
    for data in reader:                        
        if get_country_by_name(data[0]) is None:
            country = {}
            country['name'] = data[0]
            country['isoCode'] = data[1]
            country['urduName'] = data[2]
            country['addressUnitIdentifier'] = data[3]
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
                    
                
            
    
    