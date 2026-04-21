"""
Script simple para probar pandas.
Ejecutar: .venv\Scripts\python test_pandas.py
"""

import pandas as pd

# 1. Crear dataframe vacío
print("1️⃣  Crear dataframe vacío")
df = pd.DataFrame(columns=['id', 'titulo', 'ubicacion', 'tipo', 'estado'])
print(f"Columnas: {list(df.columns)}\n")

# 2. Agregar una fila con diccionario
print("2️⃣  Agregar una fila")
nueva_fila = {
    'id': 1,
    'titulo': 'Semáforo roto',
    'ubicacion': 'Calle Principal',
    'tipo': 'semaforo',
    'estado': 'abierto'
}
df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
print(df)
print()

# 3. Agregar más filas
print("3️⃣  Agregar más filas")
datos = [
    {'id': 2, 'titulo': 'Bache', 'ubicacion': 'Avenida Central', 'tipo': 'bache', 'estado': 'abierto'},
    {'id': 3, 'titulo': 'Poste caído', 'ubicacion': 'Calle 5', 'tipo': 'poste', 'estado': 'cerrado'},
]
df = pd.concat([df, pd.DataFrame(datos)], ignore_index=True)
print(df)
print()

# 4. Ver información
print("4️⃣  Información:")
print(f"Total: {len(df)} incidencias")
print(f"Tipos: {df['tipo'].unique()}")
print(f"Estados: {df['estado'].unique()}")
print()

# 5. Filtrar
print("5️⃣  Solo abiertos:")
abiertos = df[df['estado'] == 'abierto']
print(abiertos)

