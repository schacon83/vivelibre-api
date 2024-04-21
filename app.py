import logging

from src.api import app
from src.api import settings as st


if __name__ == "__main__":
    logging.info(f'{st.APP_NAME} - Starting')
    app.run(host=st.API_HOST, port=st.API_PORT)
    logging.info(f'{st.APP_NAME} - Running on port {st.API_PORT}')


