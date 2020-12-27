from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship

Base = declarative_base()

class FactCall(Base):
    __tablename__ = 'fact_call'

    id = Column(Integer, primary_key=True)
    unique_id = Column(String)
    duration = Column(SmallInteger)
    billable_duration = Column(SmallInteger)
    call_timestamp = Column(TIMESTAMP)
    dim_agent_id = Column(Integer, ForeignKey("dim_agent.id"))
    dim_deal_id = Column(Integer, ForeignKey("dim_deal.id"))
    dim_call_type_id = Column(Integer, ForeignKey("dim_call_type.id"))
    dim_disposition_id = Column(Integer, ForeignKey("dim_disposition.id"))    


class DimAgent(Base):
    __tablename__ = 'dim_agent'

    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    role_name = Column(String)
    extension = Column(SmallInteger)
    fact_calls = relationship("FactCall", backref="dim_agent", primaryjoin=id == FactCall.dim_agent_id)

    def __repr__(self):
        return self.name


class DimDeal(Base):
    __tablename__ = 'dim_deal'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    fact_calls = relationship("FactCall", backref="dim_deal", primaryjoin=id == FactCall.dim_deal_id)

    def __repr__(self):
        return self.phone_number


class DimCallType(Base):
    __tablename__ = 'dim_call_type'

    id = Column(Integer, primary_key=True)
    call_type = Column(String)
    fact_calls = relationship("FactCall", backref="dim_call_type", primaryjoin=id == FactCall.dim_call_type_id)

    def __repr__(self):
        return self.phone_number


class DimDisposition(Base):
    __tablename__ = 'dim_disposition'

    id = Column(Integer, primary_key=True)
    disposition = Column(String)
    calls = relationship("FactCall", backref="dim_disposition", primaryjoin=id == FactCall.dim_disposition_id)

    def __repr__(self):
        return self.disposition


