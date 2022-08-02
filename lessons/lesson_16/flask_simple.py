from flask import Flask

app = Flask(__name__)

@app.route('/flask')
@app.route('/')
def hel_w():
    return 'Hello, world'

if __name__ == "__main__":
    app.run()