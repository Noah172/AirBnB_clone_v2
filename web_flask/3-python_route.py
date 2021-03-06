#!/usr/bin/python3
""" This script starts a Flask web application. """
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_print(text):
    text = text.replace("_", " ")
    return "C %s" % text


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def p_print(text='is cool'):
    text = text.replace("_", " ")
    return "Python %s" % text

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
