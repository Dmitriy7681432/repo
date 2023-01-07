from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///orm.sqlite', echo = True)

Base = declarative_base()

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key = True)
    city = Column(Integer, ForeignKey('city.id'))
    sale = Column(Float)

    def __init__(self, city, sale):
        self.city = city
        self.sale = sale

    def __str__(self):
        return f'{self.city}: { self.sale}'

class Flat(Base):
    __tablename__ = 'flat'
    id = Column(Integer, primary_key = True)
    city = Column(Integer, ForeignKey('city.id'))
    floor = Column(Integer)
    rooms = Column(Integer)
    price = Column(Float)

    def __init__(self, city, floor, rooms, price):
        self.city = city
        self.floor = floor
        self.rooms = rooms
        self.price = price

    def __str__(self):
        return f'{self.city}: {self.floor}, {self.rooms}, {self.price}'

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String, unique = True)

    def __init__(self, city):
        self.city = city

    def __str__(self):
        return f'{ self.city}'

if __name__ =='__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    city = [['Moscow'], ['Kazan']]

    sale = [['Moscow', 5], ['Kazan', 3]]

    flat = [['Moscow', 5, 1, 6.2], ['Kazan', 2, 2, 5.3], ['Moscow', 16, 3, 15.6], ['Kazan', 6, 4, 10.0]]

    # session.add_all([City(x[0]) for x in city])
    # session.commit()

    # session.add_all([Sale(session.query(City).filter(City.city ==x[0]).first().id, x[1]) for x in sale])
    # session.add_all([Flat(session.query(City).filter(City.city ==x[0]).first().id, x[1], x[2],x[3]) for x in flat])
    # session.commit()

    #JOIN_________________-
    query = session.query(Flat, City)
    query =query.join(Flat, Flat.city ==City.id)
    records =query.all()

    for obj1, obj2 in records:
        print(obj1,obj2)