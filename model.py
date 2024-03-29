import datetime
import json


class Country:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.isoCode = None
        self.addressUnitIdentifier = None
        self.currency = None
        self.residenceMeasurementUnit = None

    def encode_associations(self, obj):
        if isinstance(obj, Currency):
            return obj.__dict__
        if isinstance(obj, ResidenceMeasurementUnit):
            return obj.__dict__
        return obj
        
    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.isoCode


class Gender:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None

    def __repr__(self):
        return self.name + ', ' + self.urduName


class CandidateStatusType:

    def __init__(self):
        self.id = None
        self.name = None        

    def __repr__(self):
        return self.name


class CandidateStatus:

    def __init__(self):
        self.id = None
        self.createdAt = None
        self.updatedAt = None
        self.candidateStatusType = None
        self.person = None

    def encode_associations(self, obj):        
        if isinstance(obj, CandidateStatusType):
            return obj.__dict__
        if isinstance(obj, Person):
            return obj.__dict__        
        return obj


class CityArea:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.city = None        

    def encode_associations(self, obj):
        if isinstance(obj, City):
            return obj.__dict__        
        return obj


class LanguageProficiency:

    def __init__(self):
        self.id = None
        self.name = None
        self.level = None       


class Language:

    def __init__(self):
        self.id = None
        self.name = None
        self.nativeName = None
        self.code6391 = None
        self.code6392T = None
        self.code6392B = None


class Currency:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.code = None

    def __repr__(self):
        return self.name + ', ' + self.urduName


class Ethnicity:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None        

    def __repr__(self):
        return self.name + ', ' + self.urduName


class MaritalStatus:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.genders = []

    def encode_gender(self, obj):
        if isinstance(obj, Gender):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + ' '.join(self.genders)


class EducationLevel:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class Caste:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.parent = None

    def encode_parent(self, obj):
        if isinstance(obj, Caste):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.parent.name


class AccommodationStatus:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class AccommodationType:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class Profession:

    def __init__(self):
        self.id = None
        self.name = None
        self.conceptUri = None
        self.iscoGroup = None
        self.description = None
        self.parent = None
    
    def encode_parent(self, obj):
        if isinstance(obj, Profession):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name

class EmploymentStatus:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class Religion:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class CountryAdminUnitType:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.parent = None
        self.country = None        

    def encode_associations(self, obj):
        if isinstance(obj, CountryAdminUnitType):
            return obj.__dict__
        if isinstance(obj, Country):
            return obj.__dict__        
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.parent.name + ', ' + self.country.name


class CountryAdminUnit:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.parent = None
        self.countryAdminUnitType = None

    def encode_associations(self, obj):
        if isinstance(obj, CountryAdminUnit):
            return obj.__dict__
        if isinstance(obj, CountryAdminUnitType):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.parent.name + ', ' + self.countryAdminUnitType.name


class ResidenceMeasurementUnit:

    def __init__(self):
        self.id = None
        self.name = None   

    def __repr__(self):
        return self.name + ', ' + self.urduName


class City:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.latitude = None
        self.longitude = None
        self.population = None
        self.capital = None
        self.country = None
        self.adminUnit = None
        self.residenceMeasurementUnit = None

    def encode_associations(self, obj):
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, CountryAdminUnit):
            return obj.__dict__
        if isinstance(obj, ResidenceMeasurementUnit):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName


class Sect:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.parent = None
        self.religion = None

    def encode_associations(self, obj):
        if isinstance(obj, Sect):
            return obj.__dict__
        if isinstance(obj, Religion):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.parent.name + ', ' + self.religion.name


class ContactType:

    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return self.name


class Contact:

    def __init__(self):
        self.id = None
        self.contact = None
        self.contactType = None
        self.person = None

    def encode_associations(self, obj):
        if isinstance(obj, ContactType):
            return obj.__dict__
        if isinstance(obj, Person):
            return obj.__dict__


class EducationalInstituteType:

    def __innt__(self):
        self.id = None
        self.name = None        
    

class EducationalInstitute:

    def __innt__(self):
        self.id = None
        self.name = None
        self.country = None
        self.educationInstituteType = None

    def encode_associations(self, obj):
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, EducationalInstituteType):
            return obj.__dict__


class EducationDetails:

    def __init__(self):
        self.id = None
        self.startYear = None
        self.endYear = None
        self.grade = None
        self.current = None
        self.educationLevel = None
        self.educationalInstitute = None
        self.educationCertTitle = None
        self.person = None

    def encode_associations(self, obj):
        if isinstance(obj, EducationLevel):
            return obj.__dict__
        if isinstance(obj, Person):
            return obj.__dict__


class Address:

    def __init__(self):
        self.addressLineOne = None
        self.addressLineTwo = None
        self.addressUnitIdentifierValue = None
        self.cityArea = None
        self.city = None

    def encode_associations(self, obj):
        if isinstance(obj, City):
            return obj.__dict__


class PersonRelationshipType:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None


class AccommodationDetails:

    def __init__(self):
        self.name = None
        self.urduName = None
        self.area = None
        self.residenceMeasurementUnitValue = None
        self.residentSince = None
        self.accommodationStatus = None
        self.accommodationType = None
        self.address = None
        self.person = None

    def encode_associations(self, obj):
        if isinstance(obj, AccommodationStatus):
            return obj.__dict__
        if isinstance(obj, AccommodationType):
            return obj.__dict__
        if isinstance(obj, Address):
            return obj.__dict__
        if isinstance(obj, Person):
            return obj.__dict__


class Preferences:

    def __init__(self):
        self.id = None
        self.minAge = None
        self.maxAge = None
        self.comments = None
        self.minIncome = None
        self.employmentStatuses = None
        self.professions = None
        self.accommodationTypes = None
        self.accommodationStatuses = None
        self.maritalStatuses = None
        self.sects = None
        self.religions = None
        self.countries = None
        self.cities = None
        self.educationLevels = None
        self.castes = None

    def encode_associations(self, obj):
        # print('Preferences ' + str(type(obj)))
        if isinstance(obj, EmploymentStatus):
            return obj.__dict__
        if isinstance(obj, Profession):
            return obj.__dict__
        if isinstance(obj, AccommodationType):
            return obj.__dict__
        if isinstance(obj, AccommodationStatus):
            return obj.__dict__
        if isinstance(obj, MaritalStatus):
            return obj.__dict__
        if isinstance(obj, Sect):
            return obj.__dict__
        if isinstance(obj, Religion):
            return obj.__dict__
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, City):
            return obj.__dict__
        if isinstance(obj, EducationLevel):
            return obj.__dict__
        if isinstance(obj, Caste):
            return obj.__dict__        
        # print('returning obj ' + str(type(obj)))
        return obj

class Person:

    def __init__(self):
        self.id = None
        self.name = None
        self.createdAt = None
        self.updatedAt = None
        self.candidate = True
        self.candidateContact = True
        self.siblings = None
        self.dateOfBirth = None
        self.brothers = None
        self.sisters = None
        self.monthlyIncome = None
        self.registered = None
        self.registrationDate = None
        self.height = None
        self.weight = None
        self.nativeLanguage = None
        self.comments = None
        self.religion = None
        self.sect = None
        self.caste = None
        self.incomeCurrency = None
        self.gender = None
        self.maritalStatus = None
        self.profession = None
        self.preferences = None
        self.city = None
        self.candidateCurrentStatus = None
        self.ethnicity = None

    def encode_associations(self, obj):
        # print('Person ' + str(type(obj)))
        if isinstance(obj, Religion):
            return obj.__dict__
        if isinstance(obj, Sect):
            return obj.__dict__
        if isinstance(obj, Caste):
            return obj.__dict__
        if isinstance(obj, Gender):
            return obj.__dict__
        if isinstance(obj, MaritalStatus):
            return obj.__dict__
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, Profession):
            return obj.__dict__        
        if isinstance(obj, Preferences):
            return obj.__dict__        
        if isinstance(obj, City):
            return obj.__dict__
        if isinstance(obj, Ethnicity):
            return obj.__dict__  
        # print('returning obj ' + str(type(obj)))
        return obj