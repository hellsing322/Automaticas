import pandas as pd
import numpy as np
import os
import datetime
import locale
from Conecciones import create_ftp_connection, create_postgres_connection
def validate_data_level_1(df_data,filename):

    def get_datetime_from_filename(filename):

        date_string = filename.split('_')[-1][:12]  # Obtiene la cadena de la fecha
        date_string_modified = date_string[:-4] + '0000'  # Cambia los últimos 4 dígitos a cero
        return pd.to_datetime(date_string_modified, format='%y%m%d%H%M%S')
    def get_minute_from_filename(filename):

        return int(filename.split('_')[-1][8:10])  # Obtiene el minuto del nombre del archivo
    def get_table_name(column):

        return '_' + column.split('_')[-1].replace('m', 'h')


    global fecha_toma_archivo
    fecha_toma_archivo = get_datetime_from_filename(filename)
    global minuto_archivo
    minuto_archivo = get_minute_from_filename(filename)
    locale.setlocale(locale.LC_ALL, "es_ES.utf8")
    now = datetime.datetime.now()
    mes = now.strftime("%B")
    contador = 0
    nombre_base_archivo = "Data.csv"
    nombre_archivo_csv = nombre_base_archivo

    print("_Level 1_")
    print(df_data)

    
    df_without_cdt_columns = df_data.loc[:, ~df_data.columns.str.startswith('cdt')]


    
    while os.path.exists(nombre_archivo_csv):
        contador += 1
        nombre_archivo_csv = f"{nombre_base_archivo.split('.csv')[0]}_{contador}.csv"
    #  print(contador)
    #df_without_cdt_columns.to_csv(nombre_archivo_csv, index=False)

    # Lista de estaciones y meses para los que tienes archivos de umbrales
    unique_station = df_data['Estacion'].unique()
    station = unique_station[0]
    umbrales_file = f"./Automaticas/dataUmbral/{station}_{mes.capitalize()}.rep"
    df_umbrales = pd.read_csv(umbrales_file)
    df_umbrales = df_umbrales.transpose()
    df_umbrales.columns = df_umbrales.iloc[0]
    df_umbrales = df_umbrales.iloc[1:]

    columnas_a_comparar = df_umbrales.iloc[:, 0]

    print(columnas_a_comparar)

    df_without_cdt_columns.columns = df_without_cdt_columns.columns.str.split('_').str[1]
    duplicados = df_without_cdt_columns.columns[df_without_cdt_columns.columns.duplicated()].tolist()
    print("duplicados")
    print(duplicados)
    contador = {}
    def rename_column(col):
        if col in duplicados[:1]:
            contador[col] = contador.get(col, 0) + 1
            return f"{col}_{contador[col]}"
        return col
    df_renombrado = df_without_cdt_columns.rename(columns=rename_column)
    print(df_renombrado)
  
    df2_filtered = df_renombrado[columnas_a_comparar]
    df2_filtered.to_csv(nombre_archivo_csv, index=False)
 
    df_umbrales["UMAX"] = pd.to_numeric(df_umbrales["UMAX"], errors="coerce")
    df_umbrales["UMNI"] = pd.to_numeric(df_umbrales["UMNI"], errors="coerce")
    print(df_umbrales)
    df2_filtered = df2_filtered.apply(pd.to_numeric, errors="coerce").fillna(pd.NaT)

    # Verificar si los valores están dentro de los umbrales
    df_within_umbrales = df2_filtered.copy()
    for col in df_within_umbrales.columns:
        # umbrales_col = f"{col}"
        # print(col)
        # print(umbrales_col)
        if col in df_umbrales[station].values:
            print("df_umbrales")
            mask = (df_within_umbrales[col] >= df_umbrales.loc[df_umbrales[station] == col, "UMNI"].values[0]) & (df_within_umbrales[col] <= df_umbrales.loc[df_umbrales[station] == col, "UMAX"].values[0])
            df_within_umbrales[col] = np.where(mask, df_within_umbrales[col], np.nan)

    # Crear un nuevo DataFrame con valores que cumplen los umbrales y NaN para los que no cumplen
    df_with_umbrales_check = df_within_umbrales
    # pd.set_option('display.max_columns', None)
    print(df_with_umbrales_check)
    stats = df_with_umbrales_check.agg(['count', 'mean', 'min', 'max']).T
    print(stats)
    stats = stats.reset_index().rename(columns={'index': 'column'}) 
    column = stats['column']

    for column in df_with_umbrales_check:

        stats_filtered = stats[stats['column'] == column]

        table_name = get_table_name(column)
        save_to_postgres(stats_filtered, table_name,station)
    print(stats)  # Imprime los resultados estadísticos



    return df_data, df_with_umbrales_check

def save_to_postgres(stats, table_name,station):

        conn = create_postgres_connection()
        cur = conn.cursor()
        for _, row in stats.iterrows():
            id_estacion = int(station.replace('M', ''))
            id_usuario = 0
            fecha_toma = fecha_toma_archivo  # Usa la fecha del archivo
            fecha_ingreso = pd.Timestamp.now()
            promedio = round(row['mean'], 4)

            # Consulta para actualizar la columna correspondiente al minuto con el promedio
            update_query = f"""
            UPDATE automaticas.{table_name} SET "{minuto_archivo}min" = %s
            WHERE id_estacion = %s AND fecha_toma = %s;
            """

            # Si el registro no existe, entonces inserta uno nuevo
            insert_query = f"""
            INSERT INTO automaticas.{table_name}(
                id_estacion, id_usuario, fecha_toma, fecha_ingreso, "{minuto_archivo}min", procesado_1h)
                VALUES (%s, %s, %s, %s, %s, %s);
            """

            try:
                cur.execute(update_query, (promedio, id_estacion, fecha_toma))
                if cur.rowcount == 0:  # Si no se actualizó ninguna fila, entonces inserta una nueva
                    cur.execute(insert_query, (id_estacion, id_usuario, fecha_toma, fecha_ingreso, promedio, None))
            except Exception as e:
                print(f"Error al actualizar/insertar datos: {e}" + "En la tabla  " + table_name + " Valor ",
                    str(row['mean']) + "  min ", minuto_archivo)
            continue

        conn.commit()
        cur.close()
        conn.close()