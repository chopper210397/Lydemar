import pandas as pd
import os
import gspread
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials

# ------------------------------------------------------------------------ #
#  READING DATA FROM XLSX AND UPLOADING TO A LOCAL POSTGRESQL DATABASE     #
# ------------------------------------------------------------------------ #
# How it works?. We get our data from a ERP system, we can't connect to that system with an API
# or doing webscrapping cause is not available/possible, so instead of that, "two" xlsx files are 
# downloaded, one for "sales data" and the other for "debtors data", additionaly, we will rename the file
# so the python script can recognize the path and then make all the ETL process.

###################### SALES DATA ######################
# This data comes from "Contabilidad - Reporte Detall. Ventas" section in the facturarya ERP

# Creating the connection to the database using sqlalchemy
engine = create_engine('postgresql://postgres:rufo2324@localhost:5432/postgres')

# Reading the xlsx file 
df = pd.read_excel("C:/Users/chopper/Downloads/ventas.xlsx", skiprows=1)

# Renaming the column to have a common key name  between both tables (ventas/cobranzas)
df.rename(columns = {'Serie-Núm.':'document_number'}, inplace = True)

# Replacing line break with nothing in the Sucursal column
df = df.replace(r'\n','', regex=True) 

# We can replace large sucursal names with short names, all this in a dictionary
dict = {
        'LEONCIO PRADO  H.U. MERCADO DE PRODUCTORES REGIONALES LT.39':'LEONCIO PRADO',
        'PRINCIPAL  H.U. MERCADO DE PRODUCTORES REGIONALES LT.39':'TIENDA MERCADO MAYORISTA',
        'Tienda - Nayla  H.U. MERCADO MAYORISTA DE PRODUCTORES REGIONALES LT.39':'ALMACÉN NAYDA - MERCADO MAYORISTA'
        }
df['Sucursal'] = df['Sucursal'].replace(dict)

# Eliminating columns that we dont use/need such as Vendedor cause there is only one account and Placa was eliminated, cause we dont use that variable during the work
df = df[ df.columns.drop(['Vendedor','Placa']) ]

# Now we have to convert 'Fecha documento' from an object to a datetime column type
df['Fecha documento'] = pd.to_datetime(df['Fecha documento'], format = "%d-%m-%Y")

# Uploading the data
with engine.begin() as connection:
        df.to_sql('ventas', con=connection, index_label='id', if_exists='replace')
        print('The sales data was uploaded correctly')

####################### DEBTORS DATA ######################
# This data comes from "Cuentas por Cobrar" section in the facturarya ERP

# Reading the xlsx file 

# This first xlsx contain the first one hundred rows about debtors, cause that´s how 
# our ERP give us the data
cobranza_first_100 = pd.read_excel("C:/Users/chopper/Downloads/cobros_1.xlsx", skiprows=1)
cobranza_first_100=cobranza_first_100[
        ["Fecha Registro",
        "Documento",
        "Cliente",
        "Deuda Total",
        "Abonos Total"]]

cobranza_first_100["document_number"] = cobranza_first_100["Documento"].str[15:]
cobranza_first_100["Documento"] = cobranza_first_100["Documento"].str[:13]

# This second xlsx contain the rows from one hundred onwards
cobranza_100_to_200 = pd.read_excel("C:/Users/chopper/Downloads/cobros_2.xlsx", skiprows=1)
cobranza_100_to_200=cobranza_100_to_200[
        ["Fecha Registro",
        "Documento",
        "Cliente",
        "Deuda Total",
        "Abonos Total"]]

cobranza_100_to_200["document_number"] = cobranza_100_to_200["Documento"].str[15:]
cobranza_100_to_200["Documento"] = cobranza_100_to_200["Documento"].str[:13]

# "UNION ALL" TO BOTH DATAFRAMES
cobranzas = pd.concat([cobranza_first_100,cobranza_100_to_200])

# Uploading the data
with engine.begin() as connection:
        cobranzas.to_sql('cobranzas', con=connection, index_label='id', if_exists='replace')
        print('The debtors data was uploaded correctly')


# ------------------------------------------------------------------------ #
#              SENDING DATA FROM DATAFRAME TO GOOGLESHEET                  #
# ------------------------------------------------------------------------ #
# Why?. Cause our tableau public account can't be connected to our local postgre database,
# so we have to send our data also to a googlesheet, cause is from there where our 
# dashboard gets the data.
# https://m2msupport.net/m2msupport/generate-service-account-key-in-google-cloud-platform-gcp/ 
# In the link above are some instructions about the service account steps
# This json file is now into our github project, so we have to do reference to this wherever we want/need

creds = Credentials.from_service_account_file('C:/Users/chopper/Documents/Lydemar/causal-producer-383222-4f14feab0ec1.json', 
                                              scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Replace the spreadsheet URL with your own
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1SvmemA-Ab--VYF-99akJXpV7sPjBoqAtk1PWj2DAGNw/edit#gid=1029470420')

worksheet = sheet.get_worksheet(0)

# Replace 'data' with the name of your dataframe
df = df.astype(str)
df = pd.DataFrame(df)


# Sending sale data from dataframe to VENTAS PUCALLPA googlesheet
# The tableau and looker studio dashboards are connected to VENTAS PUCALLPA googlesheet
# That is our "free database" :D
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print('Hello, ' + os.getlogin() + ' your ETL pipeline is working correctly, good job!')