import pandas as pd
import numpy as np
def validate_data_level_0(df, file_name):   
    print(df)
    expected_columns = 170
    if df.shape[1] != expected_columns:
        print(f"Advertencia: El número de columnas del archivo {file_name} no coincide con el esperado. No se puede realizar la limpieza.")
    
    # Paso 3: Convertir la columna 'fecha' a formato de fecha y hora
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d%H%M%S', errors='coerce')
    
    # Paso 4: Filtrar registros con errores en fecha y/u hora
    df = df.dropna(subset=['fecha'])
    missing_rows = df[df.isnull().any(axis=1)]  # Filtrar filas con datos faltantes
    if not missing_rows.empty:
        print(f"Advertencia: El archivo {file_name} tiene filas con datos faltantes en los índices: {list(missing_rows.index)}")
    df = df.dropna(how='any')
    
    # Nuevo filtro: Reemplazar datos no numéricos por None o Null
    columns_to_exclude = ['fecha', 'Estacion']
    numeric_columns = [col for col in df.columns if col not in columns_to_exclude]
    non_numeric_mask = ~df[numeric_columns].applymap(pd.to_numeric, errors='coerce').notna()
    non_numeric_cells = df[numeric_columns].where(non_numeric_mask)
    df[numeric_columns] = df[numeric_columns].where(~non_numeric_mask, np.nan)

    print("Inconsistencias encontradas:", "en el archivo",file_name)
    print(non_numeric_cells.stack().reset_index().rename(columns={'level_0': 'Fila', 'level_1': 'Columna', 0: 'Valor'}))
    print("__Limpio__")
    # pd.set_option('display.max_columns', None)
    print(df)
    return df