from dateutil.relativedelta import relativedelta
from config import base_url, auth_params
from model import Person, Contact, EducationDetails, Preferences
from model import AccommodationDetails, Address
import contact_type
import marital_status
import caste
import gender
import profession
import worldcities
import religion
import sect
import education_levels
import employment_status
import accommodation_status
import csv
import requests
import json
import re
import datetime

response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def import_person():
    with open("./csv/new_applicant_details.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:
            headers.update({'Content-Type': 'application/json'})
            person_gender = None
            person_marital_status = None
            person_caste = None
            person_profession = None
            person_religion = None
            person_sect = None
            person_age = None
            person_city = None
            person_date_data = datetime.datetime(2020, 10, 1, 9, 00)
            if data["Date"] is not None and data["Date"] != '':
                # todo: doesn't populate in DB, may be adding timezome info will help
                person_date_data = datetime.datetime.strptime(data["Date"],"%Y-%m-%d")                        
            if data["Gender"] is not None:
                person_gender = gender.get_gender_by_name(data["Gender"].strip())
            if data["Age"] is not None:
                if data["Age"] == 'Above 45':
                    person_age = 45
                elif data["Age"] == 'Below 20':
                    person_age = 20
                else:
                    person_age = data["Age"]
            if data["Marital Status"] is not None:
                person_marital_status = marital_status.get_marital_status_by_name(data["Marital Status"].strip())
            if data["Caste"] is not None:
                person_caste = caste.get_caste_by_name(data["Caste"].strip())
                # if person_caste is None and data["Caste"].strip() is not None and data["Caste"].strip() != '':
                #     print(data["Caste"] + ' caste not found.')
            if data["City"] is not None:
                person_city = worldcities.get_city_by_name(data["City"].strip())
            if data["Profession"] is not None:
                person_profession = profession.get_profession_by_name(data["Profession"].strip())
                if person_profession is None and data["Profession"].strip() is not None and data["Profession"].strip() != '':
                    print(data["Profession"] + ' profession not found.')
            if data["Sect"] == 'Christian':
                person_religion = religion.get_religion_by_name('Christianity')
            else:
                person_religion = religion.get_religion_by_name('Islam')
                person_sect = sect.get_sect_by_name(map_person_sect(data["Sect"].strip()))

            person = Person()
            person.name = data["Name"].strip().title()
            person.createdAt = person_date_data.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            person.updatedAt = person_date_data.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            person.gender = person_gender
            if person_age is not None and person_age != "":
                person.dateOfBirth = (datetime.datetime.now(datetime.timezone.utc) - relativedelta(years=int(person_age))).isoformat()
            person.maritalStatus = person_marital_status
            person.caste = person_caste
            person.siblings = data["Siblings"].strip()
            person.profession = person_profession
            person.monthlyIncome = re.sub("[^0-9]", "", data["Monthly Income"].strip())
            person.religion = person_religion
            person.sect = person_sect
            person.city = person_city
            if data["Comments"].strip() is not None:
                person.comments = data["Comments"].strip()

            preferences = Preferences()

            if data["Age Req"] is not None and data["Age Req"] != '':
                preferred_age = map_preferences_age(data["Age Req"].strip(), person_age)
                preferences.minAge = preferred_age['minAge']
                preferences.maxAge = preferred_age['maxAge']
            if data["Education Req"] is not None and data["Education Req"].strip() != '':
                preferred_education_levels = []
                for preferred_education_item in map_preferred_education_level(data["Education Req"].strip()):
                    preferred_education_levels \
                        .append(education_levels.get_education_level_by_name(preferred_education_item))
                preferences.educationLevels = preferred_education_levels
            if data["Preferences"] is not None:
                preferred_marital_statuses = []
                if data["Preferences"].strip() == 'Female Job Holder':
                    preferences.employmentStatuses = []
                    preferred_employment_status = employment_status.get_employment_status_by_name('Employed')
                    preferences.employmentStatuses.append(preferred_employment_status)
                else:
                    for preferred_marital_status_item in map_preferred_marital_status_level(data["Preferences"].strip()):
                        preferred_marital_statuses \
                            .append(marital_status.get_marital_status_by_name(preferred_marital_status_item))
                preferences.maritalStatuses = preferred_marital_statuses
            if data["Caste Req"] is not None and data["Caste Req"].strip() == 'Same Cast':
                preferences.castes = [person.caste]
            if data["Sect Req"] is not None:
                if data["Sect Req"].strip() != 'Any':
                    preferences.sects = [sect.get_sect_by_name(map_person_sect(data["Sect Req"]))]
            if data["Location Req"] is not None:
                preferred_cities = []
                if data["Location Req"] == 'Same City':
                    try:
                        preferred_cities.append(person.accommodationDetails.address.city)
                    except AttributeError:
                        preferred_cities.append(None)
                else:
                    preferred_cities.append(worldcities.get_city_by_name(data["Location Req"].strip()))

            preferences_json = json.dumps(preferences.__dict__,
                                          default=preferences.encode_associations)
            preferences_response = requests.post(base_url + '/api/preferences', headers=headers, data=preferences_json)
            preferences.id = (preferences_response.json())['id']            
            
            person.preferences = Preferences()
            person.preferences.id = preferences.id
            person_json = json.dumps(person.__dict__,
                                     default=person.encode_associations)
            local_response = requests.post(base_url + '/api/people', headers=headers, data=person_json)

            # create person relationships
            if local_response.status_code == 201:
                person.id = (local_response.json())['id']
                # create person contact
                if data["Mobile"] is not None and data["Mobile"].strip() != '':
                    create_person_contact(person, data["Mobile"].strip())
                # create person education details
                if data["Education"] is not None and data["Education"].strip() != '':
                    person_education_level = education_levels. \
                        get_education_level_by_name(map_education_level(data["Education"].strip()))
                    create_person_education_details(person, person_education_level)
                # create person accommodation
                if data["City"] is not None or data["House"] is not None:
                    person_accommodation_status = None
                    person_city = None
                    if data["House"] is not None:
                        person_accommodation_status = accommodation_status \
                            .get_accommodation_status_by_name(map_accommodation_status(data["House"].strip()))                    
                    create_person_accommodation_details(person, person_accommodation_status, person_city)


def create_person_contact(person, phone_number):
    person_contact = Contact()
    person_contact.contactType = contact_type.get_contact_type_by_name('Phone')
    person_contact.contact = phone_number
    person_contact.person = person
    person_contact_json = json.dumps(person_contact.__dict__,
                                        default=person_contact.encode_associations)
    requests.post(base_url + '/api/contacts', headers=headers, data=person_contact_json)


def create_person_education_details(person, person_education_level):
    person_education_details = EducationDetails()
    person_education_details.educationLevel = person_education_level
    person_education_details.person = person
    person_education_details_json = json.dumps(person_education_details.__dict__,
                                                  default=person_education_details.encode_associations)
    requests.post(base_url + '/api/education-details', headers=headers, data=person_education_details_json)


def create_person_accommodation_details(person, person_accommodation_status, person_city):
    person_accommodation_details = AccommodationDetails()
    person_address = Address()
    person_address.city = person_city
    person_address_json = json.dumps(person_address.__dict__,
                                        default=person_address.encode_associations)
    address_response = requests.post(base_url + '/api/addresses', headers=headers, data=person_address_json)
    person_address.id = (address_response.json())['id']

    person_accommodation_details.address = person_address
    person_accommodation_details.accommodationStatus = person_accommodation_status
    person_accommodation_details.person = person
    person_accommodation_details_json = json.dumps(person_accommodation_details.__dict__,
                                                      default=person_accommodation_details.encode_associations)
    requests.post(base_url + '/api/accommodation-details', headers=headers, data=person_accommodation_details_json)


def map_preferred_marital_status_level(csv_preferred_marital_statuses):
    if csv_preferred_marital_statuses == 'No Requirement':
        return []
    elif csv_preferred_marital_statuses == 'Can Marry with Divorce':
        return ["Divorced"]
    elif csv_preferred_marital_statuses == 'Single':
        return ["Single"]
    else:
        return []


def map_preferred_marital_status_level(csv_preferred_marital_statuses):
    if csv_preferred_marital_statuses == 'No Requirement':
        return []
    elif csv_preferred_marital_statuses == 'Can Marry with Divorce':
        return ["Divorced"]
    elif csv_preferred_marital_statuses == 'Single':
        return ["Single"]
    else:
        return []


def map_preferences_age(csv_preferences_age, person_age):
    if csv_preferences_age == '20-25':
        return {'minAge': 20, 'maxAge': 24}
    elif csv_preferences_age == '25-30':
        return {'minAge': 25, 'maxAge': 29}
    elif csv_preferences_age == '30-35':
        return {'minAge': 30, 'maxAge': 34}
    elif csv_preferences_age == '35-40':
        return {'minAge': 35, 'maxAge': 39}
    elif csv_preferences_age == '40-45':
        return {'minAge': 40, 'maxAge': 44}
    elif csv_preferences_age == '45-50':
        return {'minAge': 45, 'maxAge': 50}
    elif csv_preferences_age == 'Any':
        return {'minAge': person_age, 'maxAge': person_age}
    else:
        return {'minAge': '', 'maxAge': ''}


def map_person_sect(csv_sect):
    if csv_sect == 'Sunni':
        return 'Barelvi'
    elif csv_sect == 'Ahl e Hadith':
        return 'Ahl-E-Hadees'
    elif csv_sect == 'Diobandi':
        return 'Deobandi'
    elif csv_sect == 'Syed Shia':
        return 'Shia'
    elif csv_sect == 'Syed Sunni':
        return 'Deobandi'
    elif csv_sect == 'Shia':
        return 'Shia'
    else:
        return 'Other'


def map_accommodation_status(csv_accommodation_status):
    if csv_accommodation_status == 'Own':
        return 'Owner'
    elif csv_accommodation_status == 'Rent':
        return 'Rented'


def map_preferred_education_level(csv_education_preference):
    if csv_education_preference == 'Minimum BA':
        return ["Bachelors", "Masters", "M.Phil"]
    elif csv_education_preference == 'Islamic Education':
        return ["Alim/Alima"]
    elif csv_education_preference == 'Doctor':
        return ["MBBS", "BDS"]
    elif csv_education_preference == 'Min Bs/Master':
        return ["Engineering", "Masters", "M.Phil"]
    elif csv_education_preference == 'Min FA/FSc':
        return ["Inter", "Bachelors", "Masters"]
    elif csv_education_preference == 'Min Matric':
        return ["Matric", "Inter"]
    else:
        return ["None"]


def map_education_level(csv_education_name):
    if csv_education_name == 'Alma Fazla':
        return 'Alim/Alima'
    elif csv_education_name == 'Under Matric':
        return 'Elementary'
    elif csv_education_name == 'Matric':
        return 'Matric'
    elif csv_education_name == 'FA/FSc/DAE':
        return 'Inter'
    elif csv_education_name == 'BA/BSc/B.com':
        return 'Bachelors'
    elif csv_education_name == 'Bs/Master':
        return 'Masters'
    elif csv_education_name == 'CA /ACCA':
        return 'CA/ACCA'
    elif csv_education_name == '4 years Engineering':
        return 'Engineering'
    elif csv_education_name == 'LLB':
        return 'LLB'
    elif csv_education_name == 'M.Phil':
        return 'M.Phil'
    elif csv_education_name == 'PHD':
        return 'PhD'
    elif csv_education_name == 'BDS':
        return 'BDS'
    elif csv_education_name == 'MBBS':
        return 'MBBS'
