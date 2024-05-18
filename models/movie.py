from config.database import Base
from sqlalchemy import Column, Integer, String, Float

#entidad de mi base de datos
class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    raiting = Column(Float)
    category = Column(String)