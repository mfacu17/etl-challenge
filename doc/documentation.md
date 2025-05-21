# Electric Vehicles ETL Pipeline

## Project Overview

This project is a data pipeline built using Apache Airflow, Python, and PostgreSQL to extract, transform, and load electric vehicle population data into a structured database. The main goal is to automate the ingestion and cleaning process, and make the data query-ready for analytical purposes.

### Implementation logic

- The pipeline is orchestrated by an Airflow DAG named `electric_vehicles_etl`.
- Data is extracted from the url provided by the challenge.
- Data is transformed using Python and Pandas to remove nulls, fix formatting issues and ensure data integrity.
- Transformed data is loaded into a PostgreSQL database.
- SQL queries and PowerBI reports are available to answer analytical questions.

### Main challenge and solutions

- **Environment configuration:** To avoid dependency issues, a `requirements.txt` file and environment variables setup were used.
- **Data quality:** Implemented a data quality check to filter out erroneous or inconsistent values before loading the data into the database.
- **Traceability of raw data:** The raw extracted data is saved to a CSV file at the beginning of the process. This provides traceability and allows for reviewing input if needed.
- **Reproducible environments:** One challenge I encountered was ensuring that other users could run the project with minimal setup. Although I didn't fully implement a Docker solution, the process helped me learn more about containers and how Docker could simplify cross-environment execution in the future.

## Architecture and design decisions

### Technologies used

- **Apache Airflow:** Workflow orchestration and scheduling.
- **PostgreSQL:** Data storage and querying.
- **Python & Pandas:** Data cleaning and preprocessing.
- **SQLAlchemy & psycopg2:** PostgreSQL connection handling.
- **dotenv:** To manage environment variables.

### DAG tasks

1. **extract_data** - Loads RAW CSV into memory and save a csv File to maintain traceability.
2. **transform_data** - Cleans and formats the data using pandas.
3. **load_data** - Load cleaned data into PostgreSQL.

### Design decisions

- Keeping environment variables in a `.env` file to separate code from credentials.
- Using Airflow's modular task design for clarity and reusability.
- Using a virtual environment to isolate dependencies and abstract the execution environment, preventing conflicts with system-level Python packages.

## Data transformations

- Removed rows with missing key fields ('vin_prefix', 'dol_vehicle_id')
- Normalized name columns.
- Converted data types.
- Removed duplicated rows based on primary key fields.
- Extracted longitude and latitude from the 'vehicle_location' field into two separate columns to simplify usage in Power BI.

## Running the project

Go to the README.md file in the project root for detailed setup instructions.