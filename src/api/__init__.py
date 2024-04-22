import json
import logging

from flask import Flask, Response
from werkzeug.exceptions import NotFound

from src.api import settings as st

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = st.CN_STR


@app.errorhandler(Exception)
def all_exception_handler(e):
    logging.exception('Unhandled Exception: %s', e)
    return 'Internal Server Error', 500


@app.errorhandler(400)
def api_exception_400(error):
    return 'Bad request', 400


@app.errorhandler(409)
def api_exception_409(error):
    return error.description, 409


@app.errorhandler(422)
def api_exception_422(error):
    return Response(
        json.dumps(error.description), status=422, mimetype="application/json"
    )


@app.errorhandler(NotFound)
def api_exception_not_found(exception):
    return exception.description, exception.code
