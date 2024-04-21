from src.routes.school import school_api
from src.routes.movies import movies_api


def register_api_routes(app):
    app.register_blueprint(school_api)
    app.register_blueprint(movies_api)
