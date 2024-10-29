from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base_sushi = declarative_base()

class Sushi(Base_sushi):
    __tablename__ = 'Sushis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    def toJSON(self):
        return {
            'id': self.id,
            'type': self.type,
            'image': self.image,
            'price': self.price
        }
