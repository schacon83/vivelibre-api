import json
import random

from cerberus import Validator
from flask import Blueprint, Response, abort, request

from src.business.movies import process_movies_data
from src.api import settings as st


movies_api = Blueprint('movies_api', __name__)


@movies_api.route('/movies', methods=['post'])
def post_movies():
    v = Validator(
        {
            'name': {
                'type': 'string',
                'required': True,
            },
            'director': {
                'type': 'string',
                'required': False,
            },
            'ost': {
                'type': 'string',
                'required': False,
            },
            'actors': {
                "type": "list",
                "schema": {"type": "string", "required": True},
            },
            'synopsis': {
                'type': 'string',
                'required': True,
            },
            'ratings': {
                'type': 'dict',
                'required': True,
                'valuesrules': {'type': 'float'}
            }
        }
    )

    movies = request.json
    for movie in movies:
        if not v.validate(movie):
            abort(422, description=v.errors)

    return Response(
        response=json.dumps(process_movies_data(movies)),
        status=200,
        mimetype='application/json'
    )


def generate_ratings(exclusions, count=3, min_value=5.0, max_value=10.0):
    ratings = {}
    index = 0
    while index < count:
        rating = round(random.uniform(min_value, max_value), 1)
        if rating not in exclusions:
            ratings[st.REVIEWERS[index]] = rating
            exclusions.append(rating)
            index += 1
    return ratings
