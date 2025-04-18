from sqlalchemy import Column, Integer, String, Float
from .database import Base

class MultiplicationTable(Base):
    __tablename__ = "multiplication_table"

    id = Column(Integer, primary_key=True, index=True)
    number1 = Column(Integer, index=True)
    number2 = Column(Integer, index=True)
    result = Column(Integer, index=True)
