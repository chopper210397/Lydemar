import pandas as pd
from sqlalchemy import create_engine


# Creating the connection to the database
engine = create_engine('postgresql://postgres:rufo2324@localhost:5432/postgres')

# Reading the xlsx file 
df = pd.read_excel("C:/Users/chopper/Downloads/ventas.xlsx")

# uploading the data
with engine.begin() as connection:
        df.to_sql('ventas', con=connection, index_label='id', if_exists='replace')
        print('The data was uploaded correctly')
