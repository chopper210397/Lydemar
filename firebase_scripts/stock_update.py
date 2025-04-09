import csv
import pandas as pd
import firebase_admin
from google.oauth2 import service_account
import gspread
import json
import os
import google.cloud
from firebase_admin import credentials, firestore
from google.oauth2.service_account import Credentials
import psycopg2
import psycopg2.extras as extras

#############################################################################
# Código para actualizar el listado de productos de firebase hacia postgresql

# Leyendo el service account credential
cred = credentials.Certificate("firebase_scripts\ServiceAccountKey.json")

# Creando conexión a la lista productos de nuestro firebase
app = firebase_admin.initialize_app(cred)
store = firestore.client()
products_ref = store.collection(u'products')

# Get all the documents in the products collection
docs = products_ref.get()
products_list = []

# Iterate over the documents and get the 'name' attribute
for doc in docs:
  name = doc.to_dict()['name']
  products_list.append(name)

# Ordenar la lista de productos
products_list.sort()

# Connect to the PostgreSQL database
# 'postgresql://postgres:rufo2324@161.35.184.122:5432/lydemar_peruvian_delimar'
conn = psycopg2.connect(
    host="161.35.184.122",
    port="5432",
    dbname="lydemar_peruvian_delimar",
    user="postgres",
    password="rufo2324"
)

# Create a cursor
cur = conn.cursor()

# Insert the products into the database
for product in products_list:
  cur.execute(
      "INSERT INTO products (product_name) VALUES (%s)",
      (product,)
  )

# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()


###############################################################################
# UPLOAD DATA IN GROUP BY PANDAS
# Connecting googlesheet
creds = Credentials.from_service_account_file(r'C:\Users\chopper\Documents\Lydemar\business_process\causal-producer-383222-4f14feab0ec1.json', 
                                              scopes=['https://www.googleapis.com/auth/spreadsheets'])
# Reading googlesheet
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YDWs70Lbi0caJn7Qf9wNUPSKrtE1yfDLFFsf9HAA9zM/edit?usp=sharing')

worksheet = sheet.get_worksheet(0)  
df=worksheet.get_all_records()

products_data = pd.DataFrame.from_dict(df)

# Reading csv file
# products_data = pd.read_csv(r"C:\Users\chopper\Documents\Lydemar\firebase_scripts\productos_tienda - data.csv")

products_data["img"] = products_data["img"].astype(str)

unit = []
n = len(products_data)

for i in range(0, n):
    a = products_data["unit1"][i]
    b = products_data["unit2"][i]

    list1 = [a,b]
    unit.append(list1)

products_data["unit"] = unit
products_data.drop(columns= ['unit1','unit2'],inplace=True)

def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

data = products_data.to_dict(orient='records')

for batched_data in batch_data(data, 499):
    batch = store.batch()
    for data_item in batched_data:
        doc_ref = store.collection('products').document()
        batch.set(doc_ref, data_item)
    batch.commit()

print('Succesfull upload')

###############################################################################
# GET DATA FROM FIRESTORE


# UPLOAD DATA TO FIRESTORE ONE BY ONE
doc_ref.add({u'brand': u'p-ruvian mar', 
             u'category': u'vinos',
             u'img': u'test', 
             u'name': u'filete de pollo',
             u'offer': True, 
             u'price': 24, 
             u'stock': 35, 
             u'unit': ["unidad","zapato"], 
             u'unitXBox': 12
             })





#-------------------------------------------------------------------------#
# Traer data de products de firebase para actualizarlo y subirlo de golpe #
# ------------------------------------------------------------------------#
# Por lo general usamos esta parte para dejar el stock de todos los productos de firebase en cero
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os
import ast

# Ruta al archivo de credenciales
cred_path = os.path.join("firebase_scripts", "lydemar-29f4b-firebase-adminsdk-blw1a-4c417bf6c2.json")

# Leyendo el service account credential
cred = credentials.Certificate(cred_path)

# Creando conexión a la lista productos de nuestro firebase
firebase_admin.initialize_app(cred)
store = firestore.client()
products_ref = store.collection(u'products')

# Obtener todos los documentos de la colección products
docs = products_ref.get()

# Lista para almacenar los datos
products_data = []

# Recorrer todos los documentos y extraer los datos
for doc in docs:
    product = doc.to_dict()
    products_data.append(product)

# Convertir la lista de diccionarios en un DataFrame
df = pd.DataFrame(products_data)

# Asegurar que todos los valores en la columna 'id' sean cadenas y llenar valores nulos
df['id'] = df['id'].fillna('').astype(str)

# Enviamos la lista de productos a un excel para tener un backup
df.to_excel("products.xlsx", index=False)

# Eliminamos los documentos de colección products para reemplazarlos por el nuevo dataframe
for doc in docs:
    doc.reference.delete()

# En esta parte tenemos que actualizar los datos en nuestro excel local según deseemos
# Luego leemos ese excel y ese excel o dataframe modificado es lo que subirmeos a firebase
# Leemos excel modificado
df = pd.read_excel("products.xlsx")

# Convertimos los stocks a cero
df["stock"] = 0

# Convertir la columna 'unit' a listas
df['unit'] = df['unit'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Subir los nuevos datos del DataFrame a Firestore
for index, row in df.iterrows():
    product_data = row.to_dict()
    # Si no hay id, generar uno nuevo
    if not product_data['id'] or pd.isna(product_data['id']):
        new_doc_ref = products_ref.document()
        product_data['id'] = new_doc_ref.id
    products_ref.document(product_data['id']).set(product_data)

print("Documentos reemplazados exitosamente en la colección 'products'.")


