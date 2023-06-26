from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_uri = 'postgresql://postgres:postgres@localhost:5432/astelisk_db'
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
