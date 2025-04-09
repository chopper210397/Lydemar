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
from sqlalchemy import create_engine
from datetime import datetime

creds = Credentials.from_service_account_file(r'firebase_scripts\lydemar_googlesheet.json', 
                                              scopes=['https://www.googleapis.com/auth/spreadsheets'])
# Reading googlesheet
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1YTsHJWoeBouUWHKPvGzZHum_ppVPyYFeovEhoB-AqKA/edit?usp=sharing')
worksheet = sheet.worksheet('TABLA COMISIÓN ALDAIR - MASTER')
df=worksheet.get_all_records()

# Con esto ya tenemos la tabla de comisiones lista para ser usada
tabla_comisiones = pd.DataFrame.from_dict(df)

# Reading postgresql database
# Crea el engine de SQLAlchemy para PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:rufo2324@161.35.184.122:5432/lydemar_peruvian_delimar')

# Ejecutamos una consulta y cargamos el resultado en un DataFrame
query = """-- todas las ventas del mes seleccionado que entran para el cálculo de las comisiones de aldair

WITH Total_Cobrado_Documento AS (
    SELECT 
        c.numero_documento,
        SUM(c.monto) AS total_cobrado
    FROM cobranzas c
    GROUP BY c.numero_documento
),
Cobros_Ultimos_Octubre AS (
    SELECT 
        c.numero_documento,
        MAX(c.fecha) AS ultima_fecha_cobro
    FROM cobranzas c
    WHERE DATE_TRUNC('month', c.fecha) = '2024-12-01'
    GROUP BY c.numero_documento
),
Ventas_Vendedor_Aldair AS (
    SELECT 
        v.numero_documento,
        v.cliente,
        SUM(v.precio_total) AS total_venta
    FROM ventas_mayorista v
    WHERE 
        v.vendedor = 'Aldair'
    GROUP BY v.numero_documento, v.cliente
),
Ventas_a_comisionar as (
SELECT 
    v.numero_documento,
    v.cliente,
    v.total_venta,
    t.total_cobrado
FROM Ventas_Vendedor_Aldair v
JOIN Total_Cobrado_Documento t 
    ON v.numero_documento = t.numero_documento
JOIN Cobros_Ultimos_Octubre c_oct
    ON v.numero_documento = c_oct.numero_documento
WHERE 
    v.total_venta = t.total_cobrado
order by numero_documento asc   
)
select
	fecha as fecha_venta,
	cliente,
	numero_documento,
	producto,
	precio_total
from ventas_mayorista
where numero_documento  in (select distinct numero_documento  from Ventas_a_comisionar )
order by numero_documento asc, producto asc"""  # Reemplaza con tu consulta o nombre de tabla

ventas_a_comisionar = pd.read_sql_query(query, engine)

# Quitamos los espacios al final de la columna producto
ventas_a_comisionar['producto'] = ventas_a_comisionar['producto'].str.strip()

# PASO FINAL PARA CALCULAR LAS COMISIONES, UNIMOS AMBAS TABLAS
# Asegurémonos de que la columna COMISIONES esté en formato numérico (porcentaje convertido a decimal)
tabla_comisiones['COMISIONES'] = tabla_comisiones['COMISIONES'].replace('%', '', regex=True).astype(float) / 100

# Hacer el merge entre las dos tablas usando la columna 'producto'
comisiones_finales = pd.merge(ventas_a_comisionar, tabla_comisiones, how='left', left_on='producto', right_on='PRODUCTOS')

# Ahora, calculamos la comisión multiplicando el precio_total por el porcentaje de comisión
comisiones_finales['comision_calculada'] = comisiones_finales['precio_total'] * comisiones_finales['COMISIONES']

# Exportamos data de comisiones
fecha_hoy = datetime.today().strftime('%Y_%m_%d')
nombre_tabla = "comisiones_finales_vendedor_mayorista"
nombre_archivo = f"{nombre_tabla}_{fecha_hoy}.xlsx"
comisiones_finales.to_excel(nombre_archivo, index=False)
comisiones_finales["comision_calculada"].sum()
