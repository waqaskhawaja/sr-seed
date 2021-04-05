from datetime import datetime
import glob
import os
import csv
import sys
import requests
import json

base_url = 'http://localhost:9000'

auth_params = {'username':'admin','password':'admin'}
response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}

def get_gender_by_name(gender):
    response = requests.get(base_url + '/api/_search/genders', headers=headers, data={'query':gender})
    if(response.status_code) != 500:
        response = response.json()
        if len(response) > 0 and response[0] is not None and response[0]['name'] == gender:
            gender = Gender()
            gender.id = response[0]['id']
            gender.name = response[0]['name']            
            gender.urdu_name = response[0]['urduName']            
            return gender


def import_genders():
    with open("./csv/gender.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_gender_by_name(data[0]) is None:
                gender = {}
                gender['name'] = data[0]                
                gender['urduName'] = data[1]                
                response = requests.post(base_url + '/api/genders',headers=headers, json=gender)








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
                    
                
            
    
    