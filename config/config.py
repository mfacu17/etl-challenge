import os
from dotenv import load_dotenv


# Cargar el archivo .env desde la raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
RAW_TABLE_NAME = os.getenv("RAW_TABLE_NAME")
CLEAN_TABLE_NAME = os.getenv("CLEAN_TABLE_NAME")
DATA_URL = os.getenv("DATA_URL")

# Ruta absoluta basada en la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE_DIR, 'data')