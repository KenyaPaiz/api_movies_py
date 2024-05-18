import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_database = "../database.sqlite"
#leemos el directorio actual
base_dir = os.path.dirname(os.path.realpath(__file__))

#conectamos con una base de datos sqlite y asignamos la url de la bd (f -> indica que se le esta dando formato)
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_database)}"

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()