from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/main')
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/page_parser')
def page_parser():
    return render_template('page_parser.html')

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