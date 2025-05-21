from configparser import ConfigParser
from sqlalchemy import create_engine
import pandas as pd
import os

from config.config import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, DATA_PATH


def load_data():
    """Load cleaned data to a new table in PostgreSQL"""

    # Connection params to create our cleaned data table
    conn_str = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(conn_str)

    # Load DataFrame
    csv_path = f'{DATA_PATH}/electric_vehicles_cleaned_data.csv'

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV en {csv_path}.")

    df = pd.read_csv(csv_path)
    df.to_sql('electric_vehicles', engine, if_exists='replace', index=False)