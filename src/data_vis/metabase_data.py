import duckdb
import sqlite3
import pandas as pd

from config.settings import (
    DATA_DIR,
    DB_NAME,
    METABASE_DB_NAME
)

duck_conn = duckdb.connect(database=f'{DATA_DIR}/{DB_NAME}')

sqlite_conn = sqlite3.connect(f'{DATA_DIR}/{METABASE_DB_NAME}')

population_density_df = duck_conn.execute("SELECT * FROM ondoriya.gold.population_density_by_region").df()
population_density_df.to_sql('population_density_by_region', sqlite_conn, if_exists='replace', index=False)

duck_conn.close()