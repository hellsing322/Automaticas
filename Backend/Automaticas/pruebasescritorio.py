import os
import numpy as np
import pandas as pd
from Conecciones import create_ftp_connection, create_postgres_connection
from multiprocessing import Pool, Lock

pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
lock = Lock()

def get_datetime_from_filename(filename):
    """
    Obtiene la fecha y hora a partir del nombre del archivo.

    Args:
        filename (str): Nombre del archivo.

    Returns:
        pd.Timestamp: Fecha y hora extraída del nombre del archivo.
    """
    date_string = filename.split('_')[-1][:12]  # Obtiene la cadena de la fecha
    date_string_modified = date_string[:-4] + '0000'  # Cambia los últimos 4 dígitos a cero
    return pd.to_datetime(date_string_modified, format='%y%m%d%H%M%S')


def get_minute_from_filename(filename):
    """
    Obtiene el minuto a partir del nombre del archivo.

    Args:
        filename (str): Nombre del archivo.

    Returns:
        int: Minuto extraído del nombre del archivo.
    """
    return int(filename.split('_')[-1][8:10])  # Obtiene el minuto del nombre del archivo


def process_file(args):
    """
    Procesa un archivo.

    Args:
        args (tuple): Tupla que contiene el nombre del archivo y la carpeta.

    Returns:
        tuple: Tupla que contiene el DataFrame procesado y el nombre de la carpeta.
    """
    filename, folder = args
    ftp = create_ftp_connection()
    ftp.cwd(folder)

    with open(filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

    df = pd.read_csv(filename)
    print(df)

    global fecha_toma_archivo
    fecha_toma_archivo = get_datetime_from_filename(filename)
    global minuto_archivo
    minuto_archivo = get_minute_from_filename(filename)
    os.remove(filename)
    ftp.quit()

    return df, folder

def get_table_name(column):
    """
    Obtiene el nombre de la tabla basado en el número de la columna.

    Args:
        column (str): Nombre de la columna.

    Returns:
        str: Nombre de la tabla.
    """
    return '_' + column.split('_')[-1].replace('m', 'h')


def process_folder(folder):
    """
    Procesa una carpeta.

    Args:
        folder (str): Nombre de la carpeta.
    """
    lock.acquire()  # Asegura que solo un proceso pueda acceder a la carpeta a la vez
    try:
        ftp = create_ftp_connection()
        ftp.cwd(folder)

        filenames = list(filter(lambda f: f.endswith('.rep'), ftp.nlst()))
        print("__filenames___")
        print(filenames) 
        all_data_with_folder = [process_file((f, folder)) for f in filenames]
        # print("all_data_with_folder")
        # print(all_data_with_folder)
        all_data = pd.concat([df for df, _ in all_data_with_folder])
        # print("all_data")
        # print(all_data)
        numeric_columns = all_data.select_dtypes(include=np.number).columns.tolist()
        
        # Filtra las columnas numéricas seleccionadas por nombre
        filtered_columns = [col for col in numeric_columns if not col.startswith('cdt') and col != 'fecha']

        # Realiza algunas operaciones estadísticas en las columnas numéricas seleccionadas y guarda los resultados en stats
        stats = all_data.loc[:, filtered_columns].agg(['count', 'mean', 'min', 'max']).T
        
        stats = stats.reset_index().rename(columns={'index': 'column'})  # Cambia el nombre de la columna 'index' a 'column' en stats
        stats['folder'] = folder  # Agrega una columna 'folder' a stats con el nombre de la carpeta
        column = stats['column']

        for column in filtered_columns:

            stats_filtered = stats[stats['column'] == column]

            table_name = get_table_name(column)
            save_to_postgres(stats_filtered, table_name)
        print(stats)  # Imprime los resultados estadísticos

        # Filtra las columnas no numéricas en all_data
        non_numeric_data = all_data.select_dtypes(exclude=np.number)

        # Filtra las columnas no numéricas seleccionadas por nombre
        non_numeric_filtered_columns = [col for col in non_numeric_data.columns if not col.startswith('cdt') and col != 'fecha']

        non_numeric_data = non_numeric_data[non_numeric_filtered_columns]

        if not non_numeric_data.empty:  # Verifica si non_numeric_data no está vacío
            non_numeric_data = non_numeric_data.dropna(how='all')  # Elimina filas con valores nulos en non_numeric_data
            non_numeric_data = non_numeric_data.melt(var_name='column', value_name='non-numeric value')  # Transforma las columnas en filas en non_numeric_data utilizando la función melt
            non_numeric_data['folder'] = folder  # Agrega una columna 'folder' a non_numeric_data con el nombre de la carpeta
            print(non_numeric_data)  # Imprime los datos no numéricos

        ftp.cwd("..")  # Regresa al directorio principal antes de continuar con la próxima carpeta
    finally:
        lock.release()  # Libera el lock una vez que se ha terminado de procesar la carpeta


def process_folders(folders):
    """
    Procesa varias carpetas en paralelo.

    Args:
        folders (list): Lista de nombres de carpetas.
    """
    num_processes = os.cpu_count() - 1
    with Pool(processes=num_processes) as p:
        p.map(process_folder, folders)


def process_files():
    """
    Procesa los archivos en las carpetas 'M002' y 'M001'.
    """
    folders = ['M002', 'M001']
    process_folders(folders)


def save_to_postgres(stats, table_name):
    """
    Guarda los resultados estadísticos en una tabla de PostgreSQL.

    Args:
        stats (pd.DataFrame): DataFrame con los resultados estadísticos.
        table_name (str): Nombre de la tabla.
    """
    conn = create_postgres_connection()
    cur = conn.cursor()
    for _, row in stats.iterrows():
        id_estacion = int(row['folder'].replace('M', ''))
        id_usuario = 0
        fecha_toma = fecha_toma_archivo  # Usa la fecha del archivo
        fecha_ingreso = pd.Timestamp.now()
        promedio = row['mean']

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


if __name__ == '__main__':
    process_files()
