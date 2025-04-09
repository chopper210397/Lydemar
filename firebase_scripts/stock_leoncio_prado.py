import csv
import pandas as pd
import firebase_admin
from google.oauth2 import service_account
import gspread
import json
import os
import google.cloud
from firebase_admin import credentials, firestore
from firebase_scripts.vistas_stock_leoncio_prado import borrar_vista_stock_leoncio
from firebase_scripts.vistas_stock_leoncio_prado import crear_vista_stock_leoncio
from google.oauth2.service_account import Credentials
import psycopg2
import psycopg2.extras as extras
from sqlalchemy import create_engine

# Borramos vistas de stock
borrar_vista_stock_leoncio()

# Connecting googlesheet
creds = Credentials.from_service_account_file(r'firebase_scripts\lydemar_googlesheet.json', 
                                              scopes=['https://www.googleapis.com/auth/spreadsheets'])
# Reading googlesheet
client = gspread.authorize(creds)

# De momento he puesto el link de mi copia del excel depósito de laurita, la idea es que ella me de permisos de edición
# y en base a ese permiso conectarme a su excel y de ahí jalar la data
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1em71vlbd6U3A8EnQzh8OIM-aU5-gSwEuS8rY-ZMkPPA/edit?usp=sharing')

# Para poder obtener bien la hoja, no puede poner la fecha encima, tiene que comenzar directamente con las columnas y la data, la fecha podría ponerlo en otro lado
worksheet = sheet.get_worksheet(2)  
df=worksheet.get_all_records()
products_stock = pd.DataFrame.from_dict(df)

# Definimos la fecha del stock
fecha = '2025-04-03'
products_stock["fecha"] = fecha  

# Tus datos de conexión a PostgreSQL
db_host = "161.35.184.122"
db_port = "5432"
db_name = "lydemar_peruvian_delimar"
db_user = "postgres"
db_password = "rufo2324"


# Nombre de la tabla que quieres crear en PostgreSQL
table_name = 'leoncio_prado_products_stock_table'

# Crear la cadena de conexión a PostgreSQL
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Escribir el DataFrame a la tabla de PostgreSQL
try:
    products_stock.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"DataFrame 'products_stock' escrito en la tabla '{table_name}' en PostgreSQL.")
except Exception as e:
    print(f"Ocurrió un error al escribir en la base de datos: {e}")
finally:
    # Es buena práctica cerrar la conexión
    engine.dispose()
    

# Creamos la vista de stock con la nueva data de almacen
crear_vista_stock_leoncio()