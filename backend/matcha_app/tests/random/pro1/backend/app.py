from flask import Flask
app = Flask(__name__)


@app.route('http://127.0.0.1:5000/')
def hello_world():
    return "from back end, says 99"

if __name__ == '__main__':
    app.run()