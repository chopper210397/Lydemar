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

# Exportamos dataframe a postgresql, reemplazamos toda la data de la tabla desde cero
df.to_sql('ventas_tienda_mercado_mayorista_pucallpa', engine, if_exists='replace')

# Creamos la vista de comisiones con la nueva data de ventas
crear_vista_comisiones()

# Cerramos la conexión a la base de datos
connection.close()