from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import flask_ex

#Подключение к БД через sqlalchemy
engine = create_engine('sqlite:///orm1.sqlite', echo = True)
Base = declarative_base()

class Vacancy_sqlalchemy(Base):
    __tablename__ = 'vac_sqlalchemy'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    vacancy = Column(String)
    address = Column(String)
    metro = Column(String)
    corporation = Column(String)
    salary_from = Column(String)
    salary_to = Column(String)
    currency = Column(String)
    reference = Column(String)

    def __init__(self,number, vacancy, address, metro,corporation,salary_from,salary_to,currency,reference):
        self.number = number
        self.vacancy = vacancy
        self.address = address
        self.metro = metro
        self.corporation = corporation
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.reference = reference

    def __str__(self):
        return f'{self.id},{self.number},{self.vacancy},{ self.address},{self.metro},{self.corporation},\
                {self.salary_from}, {self.salary_to},{self.currency},{self.reference}'

# Base.metadata.create_all(engine)
# Session =sessionmaker(bind=engine)
# session = Session()

# session.query(Vacancy_sqlalchemy).delete()

# print('type_flask = ', type(flask_ex.vacancy_1))
# print('flask = ', flask_ex.vacancy_1)

# for vac in flask_ex.vacancy_1:
#     vac_sql = Vacancy_sqlalchemy(vac[0],vac[1],vac[2],vac[3],vac[4],vac[5],vac[6],vac[7],vac[8])
#     session.add(vac_sql)

# vac = [1,'Middle Python developer (Казань)', 'Казань, улица Островского, 87', 'Площадь Тукая', 'Колл-Тулз', 160000, '-', 'RUR', 'https://hh.ru/vacancy/70809271']
# vac1 = ['Middle Python developer (Казань)', 'Казань, улица Островского, 87', 'Площадь Тукая', 'Колл-Тулз', 160000, '-', 'RUR', 'https://hh.ru/vacancy/70809271']
# vac_sql = Vacancy_sqlalchemy(vac[0],vac[1],vac[2],vac[3],vac[4],vac[5],vac[6],vac[7],vac[8])
# vac_sql1 = Vacancy_sqlalchemy(vac1[0],vac1[1],vac1[2],vac1[3],vac1[4],vac1[5],vac1[6],vac1[7])
# session.add(vac_sql)
# session.add(vac_sql1)
# session.commit()
