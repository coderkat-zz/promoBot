from os import environ
from flask import flask

app = Flask(__name__)
app.run(environ.get('PORT'))
