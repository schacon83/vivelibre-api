import logging
import os

# Nombre de la APP
APP_NAME = 'vivelibre-api'
# IP del servidor
API_HOST = '0.0.0.0'
# Puerto en el que va a correr la API
API_PORT = 8008

# Cadena de conexión de la bbdd
# Para la prueba se almacena la información en memoria
CN_STR = 'sqlite:///:memory:'

# Rutas de ficheros de la aplicación
SRC_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
INPUTS_PATH = os.path.join(os.path.dirname(SRC_PATH), 'jsons')
SCHOOL_JSON_FILENAME = 'school.json'
MOVIES_EXTRA_JSON_FILENAME = 'movies_extra.json'

REVIEWERS = ['Letterboxd', 'Criticker', 'Empire', 'Guardian']

# Configuración del logging de la aplicación
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Configurar el handler para escribir en fichero
file_handler = logging.FileHandler('vivelibre-api.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Configurar el handler para imprimir en la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
