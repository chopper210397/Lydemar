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


cred = credentials.Certificate("firebase_scripts\ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'products')

##############################################
# UPDATE THE PRODUCTS FROM FIREBASE TO POSTGRESQL
products_ref = store.collection(u'products')

# Get all the documents in the products collection
docs = products_ref.get()
products_list = []
# Iterate over the documents and get the 'name' attribute
for doc in docs:
  name = doc.to_dict()['name']
  products_list.append(name)

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