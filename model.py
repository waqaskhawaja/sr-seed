class Country:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.isoCode = None
        self.addressUnitIdentifier = None
        
    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.isoCode


# class City(Base):
    
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String)    
#     urdu_name = Column(String)
#     country_administrative_unit_id = Column(Integer, ForeignKey("country_administrative_unit.id"))
    

# class CityArea(Base):
    
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String)    
#     urdu_name = Column(String)
#     city_id = Column(Integer, ForeignKey("city.id"))


class Gender:

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

    def encode_associations(self, obj):
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, CountryAdminUnit):
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
        self.candidate = None
        self.contactType = None

    def encode_associations(self, obj):
        if isinstance(obj, ContactType):
            return obj.__dict__
        if isinstance(obj, Candidate):
            return obj.__dict__


class EducationDetails:

    def __init__(self):
        self.startYear = None
        self.endYear = None
        self.grade = None
        self.current = None
        self.educationLevel = None
        self.educationalInstitute = None
        self.educationCertTitle = None


class AccommodationDetails:

    def __init__(self):
        self.name = None
        self.urduName = None
        self.area = None
        self.residenceMeasurementUnitValue = None
        self.residentSince = None
        self.accommodationStatus = None
        self.accommodationType = None


class Candidate:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.age = None
        self.dateOfBirth = None
        self.siblings = None
        self.brothers = None
        self.sisters = None
        self.monthlyIncome = None
        self.comments = None
        self.registered = None
        self.registrationDate = None
        self.height = None
        self.weight = None
        self.nativeLanguage = None
        self.incomeCurrency = None
        self.contacts = None
        self.preferences = None
        self.accommodationDetails = None
        self.religion = None
        self.sect = None
        self.caste = None
        self.gender = None
        self.maritalStatus = None
        self.employmentStatus = None
        self.educationDetails = None
        self.nationalities = None
        self.employmentDetails = None
        self.addresses = None
        self.residenceCity = None
        self.profession = None

    def encode_associations(self, obj):
        # print('Candidate ' + str(type(obj)))
        if isinstance(obj, Contact):
            return obj.__dict__
        if isinstance(obj, AccommodationDetails):
            return obj.__dict__
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
        if isinstance(obj, EmploymentStatus):
            return obj.__dict__
        if isinstance(obj, EducationLevel):
            return obj.__dict__
        if isinstance(obj, Country):
            return obj.__dict__
        if isinstance(obj, Profession):
            return obj.__dict__
        if isinstance(obj, EducationDetails):
            return obj.__dict__
        if isinstance(obj, City):
            return obj.__dict__
        if isinstance(obj, Preferences):
            return obj.__dict__
        return obj

    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.parent.name + ', ' + self.religion.name


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
        self.candidate = None

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
        return obj
