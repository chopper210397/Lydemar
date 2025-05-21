# ENVIAR LA DATA DE VENTAS DE FIREBASE A POSTGRESQL

# importamos libreria
from sqlalchemy import create_engine
from sqlalchemy import text
import csv
import pandas as pd
import firebase_admin
from google.oauth2 import service_account
import gspread
import json
import sys
import os
import google.cloud
from firebase_admin import credentials, firestore
from google.oauth2.service_account import Credentials
from firebase_scripts.vistas_comisiones import borrar_vistas_comisiones
from firebase_scripts.vistas_comisiones import crear_vista_comisiones
import psycopg2
import psycopg2.extras as extras
from psycopg2 import sql
from datetime import datetime

# Borramos las vistas creadas en base a la data para que no haya problemas
borrar_vistas_comisiones()

# Llamamos las credenciales de firebase y nos conectamos a ella
cred = credentials.Certificate("firebase_scripts\ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

# Creamos conexión con la base de datos postgresql mediante sqlalchemy
engine = create_engine('postgresql://postgres:rufo2324@161.35.184.122:5432/lydemar_peruvian_delimar')
connection = engine.connect()

# importamos data de firebase de ventas de la tienda de pucallpa
doc_ref = store.collection(u'ventasRegistro')
docs = doc_ref.get()

# Insertamos la data dentro de una lista que luego pasaremos a dataframe
products_list = []
for doc in docs:
  name = doc.to_dict()
  products_list.append(name)

# Convertimos la lista de ventas a dataframe
df = pd.DataFrame(products_list)

# Corregimos un error cuando el date es nulo 
df.loc[df['date'] == '', 'date'] = '2024-06-17'

# Exportamos el dataframe a un csv para poder leerlo y no tener que consumir recursos de firebase de nuevo por si se cae el proceso
fecha_hoy = datetime.today().strftime('%Y_%m_%d')
nombre_tabla = "ventas_tienda_mercado_mayorista_pucallpa"
nombre_archivo = f"{nombre_tabla}_{fecha_hoy}.csv"
df.to_csv(nombre_archivo, index=False)

# Leemos archivo csv
df = pd.read_csv(nombre_archivo)

# Subir el DataFrame a la base de datos
df.to_sql(nombre_tabla, con=engine, if_exists='replace', index=False)

# Creamos la vista de comisiones con la nueva data de ventas
crear_vista_comisiones()

# Cerramos la conexión a la base de datos
connection.close()

#----------------------------------------------------------------------

# type_map = {
#     'int64': 'BIGINT',
#     'float64': 'FLOAT',
#     'object': 'TEXT',
#     'datetime64[ns]': 'TIMESTAMP',
#     'bool': 'BOOLEAN',
#     # Puedes agregar más tipos si los necesitas
# }

# # Función para generar la sentencia CREATE TABLE
# def generate_create_table_sql(df, table_name):
#     columns_with_types = []
    
#     for col, dtype in df.dtypes.items():
#         # Obtener el tipo SQL correspondiente
#         sql_type = type_map.get(str(dtype), 'TEXT')  # Por defecto 'TEXT' si no se encuentra en el mapa
#         columns_with_types.append(f'"{col}" {sql_type}')
    
#     # Unir las columnas y tipos en una cadena
#     columns_sql = ',\n    '.join(columns_with_types)
    
#     # Sentencia CREATE TABLE
#     create_table_sql = f"""
# CREATE TABLE IF NOT EXISTS {table_name} (
#     {columns_sql}
# );
# """
    
#     return create_table_sql

# # Generar la sentencia CREATE TABLE para tu DataFrame
# table_name = 'ventas_tienda_mercado_mayorista_pucallpa'
# create_table_sql = generate_create_table_sql(df, table_name)

# # Imprimir la sentencia SQL
# print(create_table_sql)