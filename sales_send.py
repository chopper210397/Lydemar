# # # # # #
#  fields #
# # # # # #
# fecha : date                      | cant be null
# producto : str                    | cant be null
# cantidad : int                    | cant be null
# medida : str                      | cant be null
# precio unitario : float           | cant be null
# precio total : float              | cant be null
# cliente : str                     | can be null
# A very simple Flask API to start
import os
from flask import Flask, request
from google.cloud import bigquery
from flask_cors import CORS
from datetime import datetime
from pytz import timezone
import pytz

## --------------------------------------------------------
app = Flask(__name__)
CORS(app)

# gcp service account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# activating bigquery client
client = bigquery.Client()

# Define the API endpoint
@app.route('/api/v1/ventas', methods=["GET", "POST"])
def ventas():
    # Get the product, price, and quantity from the request
    fecha = request.args.get("fecha")
    producto = request.args.get("producto")
    cantidad = request.args.get("cantidad")
    medida = request.args.get("medida")
    precio_unitario = request.args.get("precio_unitario")
    precio_total = request.args.get("precio_total")
    cliente = request.args.get("cliente")

    # America/Lima
    limatz = pytz.timezone("America/Lima")

    current_time = datetime.now(limatz)
    timestamp = current_time.timestamp()

    # Create a list of rows to insert
    rows_to_insert = [
                        {
                         "fecha": fecha,
                         "producto": producto,
                         "cantidad": cantidad,
                         "medida": medida,
                         "precio_unitario": precio_unitario,
                         "precio_total": precio_total,
                         "cliente": cliente,
                         "timestamp": timestamp
                        }
                     ]

    # Insert the rows into BigQuery
    client.insert_rows_json('lydemar.lydemar_data_warehouse.ventas', rows_to_insert)

    return "Venta registrada"