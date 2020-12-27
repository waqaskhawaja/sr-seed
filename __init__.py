from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/sr_analytics"

# Create an engine instance
alchemyEngine   = create_engine(db_string, pool_recycle=3600)

# create a configured "Session" class
Session = sessionmaker(bind=alchemyEngine)