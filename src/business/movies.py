import json
import os
import random

from src.business.tools import clean_text
from src.api import settings as st


def process_movies_data(movies):
    #  1. Se parte de las peliculas que vienen por parámetro
    with open(
            os.path.join(st.INPUTS_PATH, st.MOVIES_EXTRA_JSON_FILENAME), 'r'
    ) as f:
        movies_extra = json.load(f)

    #  2. Se añaden las películas extra
    movies.extend(movies_extra)

    #  3. Se ordenan por nombre
    movies = sorted(movies, key=lambda x: x['name'])

    #  4. Se crean 3 nuevos ratings
    #  (excluyendo los actuales para que no se repitan)
    #  5. Se guardan ya todas las películas ordenadas
    #  8. Se aprovecha que se está iterando sobre las películas y sus ratings
    #  para calcular la media
    for movie in movies:
        # Se añaden los nuevos ratings
        new_movie_ratings = _generate_ratings(
            exclusions=list(movie['ratings'].values())
        )
        movie['ratings'].update(new_movie_ratings)
        # Se ordenan
        movie['ratings'] = dict(
            sorted(
                movie['ratings'].items(),
                key=lambda item: item[1],
                reverse=True
            )
        )
        # Se calcula la media
        ratings_values = list(movie['ratings'].values())
        movie['rating_mean'] = round(
            sum(ratings_values) / len(ratings_values),
            1
        )

    #  6. Limpiamos la synopsis de Titanic
    titanic_movie = next(
        movie for movie in movies if movie['name'] == 'Titanic'
    )
    titanic_movie['synopsis'] = clean_text(titanic_movie['synopsis'])

    #  7. Filtramos por actor 'Leonardo DiCaprio'
    actor = 'Leonardo DiCaprio'
    movies = [movie for movie in movies if actor in movie['actors']]

    return movies


def _generate_ratings(exclusions, count=3, min_value=5.0, max_value=10.0):
    ratings = {}
    index = 0
    while index < count:
        rating = round(random.uniform(min_value, max_value), 1)
        if rating not in exclusions:
            ratings[st.REVIEWERS[index]] = rating
            exclusions.append(rating)
            index += 1
    return ratings
