class Country:

    def __init__(self):
        self.id = None
        self.name = None
        self.urdu_name = None
        self.iso_code = None
        self.address_unit_identifier = None
        
    def __repr__(self):
        return self.name + ', ' + self.urdu_name + ', ' + self.iso_code 

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
        self.urdu_name = None
        
    def __repr__(self):
        return self.name + ', ' + self.urdu_name
