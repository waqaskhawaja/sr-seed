class Country:

    def __init__(self):
        self.id = None
        self.name = None
        self.urduName = None
        self.isoCode = None
        self.addressUnitIdentifier = None
        
    def __repr__(self):
        return self.name + ', ' + self.urduName + ', ' + self.isoCode 


class CountryAdministrativeUnit:

    def __init__(self):
        self.id = None
        self.name = None
        self.country = None
        self.parent = None


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
