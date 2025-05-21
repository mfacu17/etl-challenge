# Airflow + PostgreSQL + Python Challenge

## Description

This project is a challenge that uses **Apache Airflow** to orchestrate tasks interacting with a **PostgreSQL** database using **Python**. The workflow includes connecting to PostgreSQL, data manipulation with Pandas, and executing SQL queries.

---

## Prerequisites

To run this project, you need:

- Python 3.9
- PostgreSQL installed and running
- A PostgreSQL user with permissions to:
    - Create databases.
    - Create tables and perform CRUD operations.
- pip
- Virtualenv to create a Python environment (Recommended)

---

## Software versions

- Python: 3.9.22
- Apache Airflow: 2.7.3
- PostgreSQL: 14.17
- Other dependencies as listed in `requirements.txt`

## Installation


1. **Clone this repository**
```bash
git clone https://github.com/mfacu17/etl_challenge.git
```
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.9.txt -r requirements.txt

```

4. Install the project in editable mode

This step enables local import of our own modules inside DAGs and scripts.
```bash
pip install -e .
```


---

## Environment variables

Before running the project, you need to manually configure the environment variables. These are used to connect to PostgreSQL database and other settings.

Create a `.env` file in the root folder with the following content:

```env
POSTGRES_USERNAME = <your_postgres_user>
POSTGRES_PASSWORD = <your_postgres_password>
POSTGRES_HOST = <postgres_host> # e.g. localhost
POSTGRES_PORT = <postgres_port> # default is 5432
POSTGRES_DB = electric_vehicles_db
RAW_TABLE_NAME = raw_electric_vehicles
CLEAN_TABLE_NAME = electric_vehicles
DATA_URL = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"
```

> **Note:** The postgresql must have permissions to create databases and tables.

---

## DAG Structure

The DAG `electric_vehicles_etl` is designed to:

- Extract data and load it to a raw table into PostgreSQL.
- Transform and clean the data using Python and Pandas.
- Load the cleaned data into PostgreSQL tables.

The DAG consists of the following tasks:
1.**extract_data**
2.**transform_data**
3.**load_data**


## Usage

1. Define airflow_home
```bash
export AIRFLOW_HOME=$(pwd)/airflow_home
```

2. Initialize airflow
```bash
airflow db init
```

3. Run the scheduler and webserver

Open separate terminals and run:

```bash
airflow scheduler
```

```bash
airflow webserver --port 8080
```

4. Load the DAG and execute it from the web interface

- Open your browser at [http://localhost:8080](http://localhost:8080).
- Find the DAG `electric_vehicles_etl`.
- Run it manually or schedule its execution.

## Using the SQL Queries File

This project includes a file named `queries.sql` which contains SQL queries answering specific questions related to the dataset.

### How to use it

1. Make sure your PostgreSQL database is running and you have connected to the correct database.

2. From the command line, you can run the queries file like this:
```bash
psql -h <host> -U <user> -d <database_name> -f queries.sql
```

Replace <host>, <user>, <database_name> with your PostgreSQL credentials.

3. Alternatively, open the queries file in your preferred SQL client and execute it manually.

**Note:** The tables and data must be loaded in the database before running these queries. Make sure to run the `electric_vehicles_etl` DAG first to load the data.


## Considerations

- Make sure your PostgreSQL user has permissions to create the specified database.
- PostgreSQL are managed via environment variables.
- The `.env` file **should not** be pushed to public repositories to avoid exposing credentials.
