import logging

from flask import Flask

from src.api import settings as st

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = st.CN_STR


@app.errorhandler(Exception)
def all_exception_handler(e):
    logging.exception('Unhandled Exception: %s', e)
    return 'Internal Server Error', 500
