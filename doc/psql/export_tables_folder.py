# Autor: Jorge Marqués 
# Fecha: 2024-07-22

import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Nombre de la carpeta y verificar que no exista
folder_name="folder"
if os.path.exists(folder_name):
    print(f"Error: La carpeta '{folder_name}' ya existe. Por favor, introduce un nombre diferente.")
    exit()
else:
    os.makedirs(folder_name)
#if

# Fecha y hora de inicio
start_date_str = "2020-01-01 00:00:00"
try:
    start_datetime = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
except ValueError:
    print("Formato de fecha y hora incorrecto. Por favor, usa el formato YYYY-MM-DD HH:MM:SS.")
    exit()
#try

# Fecha y hora de fin
end_date_str = "2026-01-01 00:00:00"
try:
    end_datetime = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    if end_datetime < start_datetime:
        print("La fecha y hora de fin no puede ser anterior a la fecha y hora de inicio.")
        exit()
except ValueError:
    print("Formato de fecha y hora incorrecto. Por favor, usa el formato YYYY-MM-DD HH:MM:SS.")
    exit()
#try

# Crear la conexión usando SQLAlchemy
engine = create_engine('postgresql+psycopg2://iaxo:bujaruelo@127.0.0.1:5432/iaxod0slowctldb')

# Conectar a la base de datos
conn = engine.connect()

# Obtener los nombres de todas las tablas
query = text("""
    SELECT table_name 
    FROM information_schema.tables
    WHERE table_schema='public'
""")
tables = conn.execute(query).fetchall()

# Bandera para verificar si se encontraron datos
data_found = False

# Descargar cada tabla en un archivo CSV
for table in tables:
    table_name = table[0]
    
    # Obtener los nombres de las columnas de la tabla
    columns_query = text(f"""
        SELECT column_name 
        FROM information_schema.columns
        WHERE table_name = :table_name
    """)
    columns = conn.execute(columns_query, {"table_name": table_name}).fetchall()
    column_names = [col[0] for col in columns]
    
    # Determinar el nombre de la columna de fecha y hora
    date_column = None
    if 'timestamp' in column_names:
        date_column = 'timestamp'
    elif 'trip_time' in column_names:
        date_column = 'trip_time'
    
    # Si no se encuentra una columna de fecha y hora, informar al usuario y continuar
    if date_column is None:
        print(f"La tabla '{table_name}' no contiene una columna reconocida para la fecha y hora.")
        continue
    
    # Leer los datos de la tabla filtrando por el rango de fecha y hora especificadas
    query = text(f"SELECT * FROM {table_name} WHERE {date_column} BETWEEN :start_datetime AND :end_datetime")
    df = pd.read_sql(query, conn, params={"start_datetime": start_datetime, "end_datetime": end_datetime})

    if not df.empty:
        df.to_csv(os.path.join(folder_name, f'{table_name}.csv'), index=False)
        data_found = True
    else:
        print(f"No se encontraron datos para la tabla '{table_name}' en el rango de fecha y hora especificado.")

# Cerrar la conexión
conn.close()

if not data_found:
    print("No se encontraron datos en ninguna tabla para el rango de fechas y horas especificado.")
else:
    print(f"Archivos CSV guardados en la carpeta: {folder_name}")


