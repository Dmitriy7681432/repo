from flask import Flask, render_template,request,redirect
from parser_hh import pars_hh
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

@app.route('/vacansies')
def vacancy():
    global city, position
    vacancy = list(pars_hh(position,city))
    # print(vacancy)
    vacancy_lst =[]
    vacancy_lst1 =[]
    for elem in vacancy:
         vacancy_lst.append('     '.join(map(str,elem)))
    vacancy_lst1.append(vacancy_lst)
    # print(vacancy_lst1)
    # print('\n')
    # print(vacancy)
    return render_template('vacansies.html',vacancy=vacancy)

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