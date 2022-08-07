from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/main')
@app.route('/')
def hel_w():
    # return 'Hello, world'
    return render_template('main.html')

@app.route('/cars')
def cars():
    model = 'Volvo'
    price = 1.5
    data ={'model':'Volvo',
           'price':1.5}
    # return 'This is contact page'
    # return render_template('contacts.html', model = model, price = price)
    return render_template('cars.html', data = data)

@app.route('/moto')
def moto():
    data ={'model':'BMW',
           'price':0.8}
    # return 'This is contact page'
    return render_template('moto.html',**data)

@app.route('/cars_form',methods=['POST'])
def cars_form():
    brand =request.form['brand']
    price =request.form['price']
    data ={'model':brand,
           'price':price}
    return render_template('cars_form.html', data = data)

if __name__ == "__main__":
    app.run(debug = True)