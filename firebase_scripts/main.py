import csv
import pandas as pd
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_scripts\ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
doc_ref = store.collection(u'products')


# GET DATA FROM FIRESTORE
try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')

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

###############################################################################
# UPLOAD DATA IN GROUP BY PANDAS

# Reading csv file
products_data = pd.read_csv(r"C:\Users\chopper\Documents\Lydemar\firebase_scripts\productos_tienda - data.csv")

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
try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')

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