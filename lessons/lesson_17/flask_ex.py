from flask import Flask, render_template,request,redirect
from parser_hh import pars_hh
import sqlite3 as lite
import sys

app = Flask(__name__)
city = 0
position =0

@app.route('/main')
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/page_parser',methods =['POST', 'GET'])
def page_parser():
    if request.method == 'POST':
        global city, position
        city = request.form['City']
        position = request.form['Position']

        return redirect('/vacansies')
    else:
        return render_template('page_parser.html')

def func_vac(x):
    return x
@app.route('/vacansies')
def vacancy():
    global city, position
    vacancy_1 =[]
    #Подлключение БД
    # connect = None
    # try:
    #     connect =lite.connect('vacancy.db')
    #
    #     cur =connect.cursor()
    #     cur.execute('SELECT SQLITE_VERSION()')
    #
    #     data = cur.fetchone()[0]
    #
    #     print(f'SQLite version: {data}')
    #
    # except lite.Error as e:
    #     print(f"Error {e.args[0]}:")
    #     sys.exit(1)

    # cur.execute('CREATE TABLE vacancy(number INT, vacancy TEXT, address TEXT, metro INT, corporation TEXT, salary_from INT, salary_to INT, currency TEXT, reference TEXT )')

    vacancy_1 = pars_hh(position,city)
    print('type_vacancy_1 = ', type(vacancy_1))
    print('vacancy_1 = ', vacancy_1)

    #Добавление в бд через ORM sqlalchemy
    # import vacancy_sqlalchemy
    # from sqlalchemy.orm import sessionmaker
    # # vacancy_sqlalchemy.Base.metadata.drop_all(vacancy_sqlalchemy.engine)
    # vacancy_sqlalchemy.Base.metadata.create_all(vacancy_sqlalchemy.engine)
    # Session =sessionmaker(bind=vacancy_sqlalchemy.engine)
    # session = Session()
    # for vac in vacancy_1:
    #     vac_sql = vacancy_sqlalchemy.Vacancy_sqlalchemy(vac[0],vac[1],vac[2],vac[3],vac[4],vac[5],vac[6],vac[7],vac[8])
    #     session.add(vac_sql)
    # session.commit()


    #Добавление в бд не через ORM
    # for vac in vacancy:
    #     cur.execute("INSERT INTO vacancy VALUES(?,?,?,?,?,?,?,?,?)",(vac[0],vac[1],vac[2],vac[3],vac[4],vac[5],vac[6],vac[7],vac[8]))
    #
    # connect.commit()
    # connect.close()

    # vacancy = list(pars_hh(position,city))
    # print(vacancy)
    # vacancy_lst =[]
    # vacancy_lst1 =[]
    # for elem in vacancy_1:
    #      vacancy_lst.append('     '.join(map(str,elem)))
    #
    # vacancy_lst1 = [vacancy_lst]
    # # print(vacancy_lst1)
    # ard = [['1','Prgram','Python']]
    # # return render_template('vacansies.html',vacancy=vacancy_lst1)
    #
    # #vacancy_lst1.append(vacancy_lst)
    #
    # # print(vacancy_lst1)
    # # print('\n')
    # # print(vacancy)
    return render_template('vacansies.html',vacancy=vacancy_1)


# @app.route('/vacansies')
# def vacancy1():
#     global city, position
#     vacancy = list(pars_hh(position,city))
#     # print(vacancy)
#     vacancy_lst =[]
#     vacancy_lst1 =[]
#     for elem in vacancy:
#          vacancy_lst.append('     '.join(map(str,elem)))
#     vacancy_lst1.append(vacancy_lst)
#     print(vacancy_lst1)
#     print('\n')
#     print(vacancy)
#     return render_template('vacansies.html',vacancy1=vacancy)

@app.route('/my_info')
def my_info():
    return render_template('my_info.html')

@app.route('/wood')
def wood():
    return render_template('wood.html')

@app.route('/dsp')
def dsp():
    return render_template('dsp.html')

@app.route('/dvp')
def dvp():
    return render_template('dvp.html')



if __name__ == "__main__":
    app.run(debug = True)
