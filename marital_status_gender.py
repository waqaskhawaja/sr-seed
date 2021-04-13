from config import base_url, auth_params
import marital_status
import gender
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token, 'Connection': None, 'Accept-Encoding': None,
           'Content-type': 'application/json'}


def import_marital_status_genders():
    with open("./csv/marital_status_gender.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            genders = []
            m_status = marital_status.get_marital_status_by_name(data[0].strip())
            gen_list = data[1].strip().split("|")
            for gen_item in gen_list:
                genders.append(gender.get_gender_by_name(gen_item.strip()))
            if m_status is not None and genders is not None and len(genders) > 0:
                m_status.genders = genders
                request_json: json = json.dumps(m_status.__dict__, default=m_status.encode_gender)
                requests.put(base_url + '/api/marital-statuses/' + str(m_status.id),
                             headers=headers, data=request_json)
