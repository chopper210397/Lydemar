# Importamos librerias
import psycopg2
from psycopg2 import sql
import os

def borrar_vista_stock_leoncio():   
    # Configuración de la conexión
    db_config = {
        'dbname': 'lydemar_peruvian_delimar',
        'user': 'postgres',
        'password': 'rufo2324',
        'host': '161.35.184.122',
        'port': '5432'
    }

    # Crear una conexión a la base de datos
    conn = psycopg2.connect(**db_config)

    # Crear un cursor para ejecutar las consultas
    cur = conn.cursor()

    # Definir las consultas para eliminar las vistas
    drop_view_queries = [
        sql.SQL("DROP VIEW IF EXISTS {}").format(sql.Identifier('stock_leoncio_prado_actualizado_view'))
    ]

    try:
        # Ejecutar cada consulta
        for query in drop_view_queries:
            cur.execute(query)
        
        # Confirmar los cambios en la base de datos
        conn.commit()
        print("Vistas eliminadas exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        # Revertir los cambios en caso de error
        conn.rollback()
    finally:
        # Cerrar el cursor y la conexión
        cur.close()
        conn.close()

def crear_vista_stock_leoncio():
    # Configuración de la conexión
    db_config = {
        'dbname': 'lydemar_peruvian_delimar',
        'user': 'postgres',
        'password': 'rufo2324',
        'host': '161.35.184.122',
        'port': '5432'
    }

    # Ruta al archivo SQL
    sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'POSTGRESQL', 'stock_leoncio_prado_actualizado_view.sql')

    # Leer el contenido del archivo SQL
    with open(sql_file_path, 'r') as file:
        create_view_query = file.read()

    try:
        # Crear una conexión a la base de datos
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Ejecutar la consulta para crear la vista
        cur.execute(create_view_query)
        
        # Confirmar los cambios en la base de datos
        conn.commit()
        
        print("Vista creada exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        # Revertir los cambios en caso de error
        conn.rollback()
    finally:
        # Cerrar el cursor y la conexión
        cur.close()
        conn.close()