# Autor: Jorge Marqués 
# Fecha: 2024-07-22
# Review: Angel Rodriguez (From export folders to plot table)

import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Fecha y hora de inicio
start_date_str = "2025-09-22 00:00:00"
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
table_name = "memory"
date_column = 'timestamp'
val_column = 'measurepoint'


# Obtener los nombres de las columnas de la tabla
columns_query = text(f"""
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_name = :table_name
""")
columns = conn.execute(columns_query, {"table_name": table_name}).fetchall()
column_names = [col[0] for col in columns]

# Determinar el nombre de la columna de fecha y hora

query = text(f"SELECT * FROM {table_name} WHERE {date_column} BETWEEN :start_datetime AND :end_datetime")
df = pd.read_sql(query, conn, params={"start_datetime": start_datetime, "end_datetime": end_datetime})

if not df.empty:
    plt.plot(df[date_column], df[val_column])
    plt.xlabel("Timestamp")
    plt.ylabel("Value (a.u.)")
    plt.xticks(rotation=45, ha='right')
    plt.grid()
    plt.tight_layout()

    plt.show()
else:
    print(f"No se encontraron datos para la tabla '{table_name}' en el rango de fecha y hora especificado.")

# Cerrar la conexión
conn.close()



