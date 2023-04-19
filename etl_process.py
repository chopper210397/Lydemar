import pandas as pd
from sqlalchemy import create_engine

###################### SALES DATA ######################
# This data comes from "Contabilidad - Reporte Detall. Ventas" section in the facturarya ERP

# Creating the connection to the database using sqlalchemy
engine = create_engine('postgresql://postgres:rufo2324@localhost:5432/postgres')

# Reading the xlsx file 
df = pd.read_excel("C:/Users/chopper/Downloads/ventas.xlsx", skiprows=1)

# uploading the data
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


# This second xlsx contain the rows from one hundred onwards
cobranza_100_to_200 = pd.read_excel("C:/Users/chopper/Downloads/cobros_2.xlsx", skiprows=1)
cobranza_100_to_200=cobranza_100_to_200[
        ["Fecha Registro",
        "Documento",
        "Cliente",
        "Deuda Total",
        "Abonos Total"]]

# "UNION ALL" TO BOTH DATAFRAMES
cobranzas = pd.concat([cobranza_first_100,cobranza_100_to_200])

# uploading the data
with engine.begin() as connection:
        cobranzas.to_sql('cobranzas', con=connection, index_label='id', if_exists='replace')
        print('The debtors data was uploaded correctly')