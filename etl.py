from model import FactCall, DimAgent, DimDeal, DimDisposition, DimCallType
from __init__ import Session
from datetime import datetime
import pandas as pd
import glob
import os
import psycopg2
import csv
import sys

# create a Session
session = Session()

path = r'./csv' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

def create_deal(phone_number):
    deal = DimDeal()
    deal.phone_number = phone_number
    session.add(deal)
    session.commit()
    return deal


for filename in all_files:
    with open(filename, newline='') as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_file, None)
        call_type = DimCallType()
        deal = DimDeal()
        disposition = DimDisposition()        
        for row in csv_file:
            call = FactCall()
            try:                
                disposition = session.query(DimDisposition).filter(DimDisposition.disposition==row[11]).first()
                # Check if it is an incoming call
                # if row[4] == 'ext-local' or row[4] == 'from-queue-exten-internal':
                if row[4] == 'none calls':
                    call_type = session.query(DimCallType).filter(DimCallType.call_type=='Incoming').first()
                    agent = session.query(DimAgent).filter(DimAgent.extension==int(row[3])).first()
                    # check if deal exists
                    deal = session.query(DimDeal).filter(DimDeal.phone_number==row[2]).first()
                    if deal is None:
                        deal = create_deal(row[2])
                        
                    call.unique_id =  row[14]
                    call.duration = int(row[9])
                    call.billable_duration = int(row[10])         
                    call.call_timestamp =  datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")    
                    call.dim_agent_id = agent.id
                    call.dim_deal_id = deal.id
                    call.dim_call_type_id = call_type.id
                    call.dim_disposition_id = disposition.id
                    session.add(call)
                    session.commit()
                elif row[4] == 'from-internal':
                    call_type = session.query(DimCallType).filter(DimCallType.call_type=='Outgoing').first()
                    agent = session.query(DimAgent).filter(DimAgent.extension==int(row[2])).first()
                    # check if deal exists
                    deal = session.query(DimDeal).filter(DimDeal.phone_number==row[3]).first()
                    if deal is None:
                        deal = create_deal(row[3])
                        
                    call.unique_id =  row[14]
                    call.duration = int(row[9])
                    call.billable_duration = int(row[10])         
                    call.call_timestamp =  datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")    
                    call.dim_agent_id = agent.id
                    call.dim_deal_id = deal.id
                    call.dim_call_type_id = call_type.id
                    call.dim_disposition_id = disposition.id
                    session.add(call)
                    session.commit()
            except:
                session.rollback()
                print("Unexpected error:", sys.exc_info()[0])
                print(', '.join(row))
            finally:
                session.close()
    
    # li = []
    # df = pd.read_csv(filename, index_col=None, header=0)
    # li.append(df)

# frame = pd.concat(li, axis=0, ignore_index=True)

# print(frame.info())