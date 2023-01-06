from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///orm.sqlite', echo = True)

Base = declarative_base()

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    model = Column(String)
    price = Column(Float)
    city = Column(String)

    def __init__(self, model, price, city):
        self.model = model
        self.price = price
        self.city = city

    def __str__(self):
        return f'{self.id},{ self.model},{self.price},{self.city}'

Base.metadata.create_all(engine)

Session =sessionmaker(bind=engine)
session = Session()

car_1 = Car('Volvo', 5000,'Moscow')
car_2 = Car('Nissan', 6000,'Kazan')

session.add(car_1)
session.add(car_2)

session.commit()

cars_query =session.query(Car)
print(type(cars_query))
for car in cars_query:
    print(car)