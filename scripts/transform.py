import pandas as pd
import re
import os
import logging

from config.config import DATA_PATH

logger = logging.getLogger(__name__)

def normalize_column(column_name):
    """Function that normalizes column names deleting blank spaces and uppercase"""
    
    column_name = column_name.strip().lower()
    column_name = re.sub(r'\s', '_', column_name)
    column_name = re.sub(r'[^\w]', '', column_name)

    # Personalized rule for 'VIN (1-10)'
    if re.match(r'^vin.*', column_name):
        return 'vin_prefix'
    
    if 'cafv' in column_name:
        return 'clean_fuel_vehicle_eligibility'

    if 'census' in column_name:
        return 'census_tract_2020' 

    return column_name

def transform_data():
    """Clean some nulls, duplicateds and fix data types """

    logger.info('Transformation initiated')

    # Load DataFrame
    csv_path = f"{DATA_PATH}/electric_vehicles_raw_data.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV en {csv_path}.")

    df = pd.read_csv(csv_path)

    print(df.describe(include='all'))

    print("\n=============== NULL COUNT ================= ")
    print(df.isna().sum().sort_values(ascending=False))

    # Apply last function to every column
    df.columns = [normalize_column(col) for col in df.columns]

    # Impute missing values only for columns where we know it won't affect statystical analyses.
    df.fillna({
        'county':'Unknown',
        'city':'Unknown',
        'state': 'XX',
        'make':'UNKNOWN',
        'model':'UNKNOWN',
        'electric_vehicle_type':'Unknown',
        'clean_alternative_fuel_vehicle_cafv_eligibility':'Unknown',
        'vehicle_location': 'Unknown',
        'electric_utility': 'Unknown'
    },inplace=True)

    # Drop rows where key identifiers are missing
    df = df.dropna(subset=['vin_prefix', 'dol_vehicle_id'])

    # Fix column types
    df['model_year'] = df['model_year'].astype(int)
    df['electric_range'] = pd.to_numeric(df['electric_range'], errors='coerce')
    df['base_msrp'] = pd.to_numeric(df['base_msrp'], errors='coerce')
    df['postal_code'] = df['postal_code'].astype('Int64').astype(str)
    df['census_tract_2020'] = df['census_tract_2020'].astype('Int64').astype(str)
    df['legislative_district'] = df['legislative_district'].astype('Int64').astype(str)

    # 'vehicle_location' divide
    df[['longitude', 'latitude']] = df['vehicle_location'].str.extract(
        r'POINT \((-?\d+\.\d+)\s+(-?\d+\.\d+)\)'
    )
    df['latitude'] = pd.to_numeric(df['latitude'],errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'],errors='coerce')


    df.drop_duplicates(subset=['vin_prefix', 'dol_vehicle_id'],inplace=True)

    try:
        output_path = f"{DATA_PATH}/electric_vehicles_cleaned_data.csv"
        df.to_csv(output_path, index=False)
        logger.info(f'Cleaned csv saved successfully in: {output_path}')
    except Exception as e:
        logger.error(f"Error saving csv file: {e}")
