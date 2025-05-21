import os
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import io
import logging
    
from config.config import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, DATA_URL, RAW_TABLE_NAME, DATA_PATH

logger = logging.getLogger(__name__)

def create_database():
    """Create a new database where we're going to work with the dataset"""

    # Create the connection to a default database with an user with CREATEDB privilege
    conn = psycopg2.connect(
        dbname = 'postgres',
        user = POSTGRES_USERNAME,
        password = POSTGRES_PASSWORD,
        host = POSTGRES_HOST,
        port = POSTGRES_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create a new database where we're going to work with our dataset
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (POSTGRES_DB,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")
        logger.info(f"Database {POSTGRES_DB} created successfully!")
    else:
        logger.info(f"Database {POSTGRES_DB} already exists!")
    
    # Close connections
    cursor.close()
    conn.close()

def extract_data():
    """Read the raw dataset and load it in a new table"""

    create_database()

    # Read the dataset
    response = requests.get(DATA_URL)
    response.raise_for_status()

    # Create our Pandas DataFrame
    df = pd.read_csv(io.StringIO(response.text))

    # Save csv locally
    os.makedirs(DATA_PATH, exist_ok=True)
    csv_path = f"{DATA_PATH}/electric_vehicles_raw_data.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"Raw data successfully saved in '{csv_path}'!")

    # Connect to the database we created
    conn_str = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(conn_str)

    # Create the raw data table
    df.to_sql(RAW_TABLE_NAME, engine, if_exists='replace', index=False)
    logger.info(f"Table {RAW_TABLE_NAME} created successfully with raw data")