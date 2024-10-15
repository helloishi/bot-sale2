from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'user_user'
    
    username = Column(String, primary_key=True, index=True)
    name = Column(String)
    
