import os
import numpy as np
import pandas as pd
from Conecciones import create_ftp_connection  # Importa la función create_ftp_connection del módulo Conecciones
from multiprocessing import Pool  # Importa la clase Pool del módulo multiprocessing

pd.set_option('display.max_rows', None)  # Configura pandas para mostrar todas las filas al imprimir un DataFrame

def process_file(args):
    # La función process_file recibe los argumentos filename (nombre del archivo) y folder (carpeta en el servidor FTP)
    filename, folder = args
    ftp = create_ftp_connection()  # Crea una conexión FTP utilizando la función create_ftp_connection
    ftp.cwd(folder)  # Navega al directorio especificado por folder en el servidor FTP
    
    # Descarga el archivo desde el servidor FTP y guarda su contenido localmente
    with open(filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

    df = pd.read_csv(filename)  # Lee el archivo CSV descargado en un DataFrame de pandas llamado df

    os.remove(filename)  # Elimina el archivo descargado localmente
    ftp.quit()  # Cierra la conexión FTP
    return df, folder  # Devuelve el DataFrame df y el nombre de la carpeta folder

def process_folders(folders, index=0):
    # La función process_folders recibe la lista de carpetas (folders) y un índice opcional (index) para rastrear la posición actual en la lista
    if index < len(folders):
        folder = folders[index]
        ftp = create_ftp_connection()  # Crea una conexión FTP utilizando la función create_ftp_connection
        ftp.cwd(folder)  # Navega al directorio de la carpeta actual en el servidor FTP

        filenames = list(filter(lambda f: f.endswith('.rep'), ftp.nlst()))  # Obtiene una lista de nombres de archivos que terminan con la extensión '.rep' en la carpeta
        num_processes = os.cpu_count() - 1
        with Pool(processes=num_processes) as p:  # Inicia una instancia de Pool para procesar los archivos en paralelo
            all_data_with_folder = p.map(process_file, [(f, folder) for f in filenames])  # Procesa los archivos en paralelo utilizando la función process_file

        all_data = pd.concat([df for df, _ in all_data_with_folder])  # Concatena los DataFrames resultantes en all_data

        # Filtra las columnas numéricas en all_data
        numeric_columns = all_data.select_dtypes(include=np.number).columns.tolist()

        # Filtra las columnas numéricas seleccionadas por nombre
        filtered_columns = [col for col in numeric_columns if not col.startswith('cdt') and col != 'fecha']

        # Realiza algunas operaciones estadísticas en las columnas numéricas seleccionadas y guarda los resultados en stats
        stats = all_data.loc[:, filtered_columns].agg(['count', 'mean', 'min', 'max']).T
        stats = stats.reset_index().rename(columns={'index': 'column'})  # Cambia el nombre de la columna 'index' a 'column' en stats
        stats['folder'] = folder  # Agrega una columna 'folder' a stats con el nombre de la carpeta
        print(stats)  # Imprime los resultados estadísticos

        # Filtra las columnas no numéricas en all_data
        non_numeric_data = all_data.select_dtypes(exclude=np.number)

        # Filtra las columnas no numéricas seleccionadas por nombre
        non_numeric_filtered_columns = [col for col in non_numeric_data.columns if not col.startswith('cdt') and col != 'fecha']

        non_numeric_data = non_numeric_data[non_numeric_filtered_columns]  # Filtra las columnas no numéricas seleccionadas en non_numeric_data
        
        if not non_numeric_data.empty:  # Verifica si non_numeric_data no está vacío
            non_numeric_data = non_numeric_data.dropna(how='all')  # Elimina filas con valores nulos en non_numeric_data
            non_numeric_data = non_numeric_data.melt(var_name='column', value_name='non-numeric value')  # Transforma las columnas en filas en non_numeric_data utilizando la función melt
            non_numeric_data['folder'] = folder  # Agrega una columna 'folder' a non_numeric_data con el nombre de la carpeta
            print(non_numeric_data)  # Imprime los datos no numéricos

        ftp.cwd("..")  # Regresa al directorio principal antes de continuar con la próxima carpeta
        process_folders(folders, index + 1)  # Llama recursivamente a process_folders para procesar la próxima carpeta en la lista folders

def process_files():
    # La función process_files se encarga de iniciar el procesamiento de las carpetas
    folders = ['M002', 'M001']  # Lista de nombres de carpetas conocidas
    process_folders(folders)  # Llama a la función process_folders para procesar las carpetas

if __name__ == '__main__':
    process_files()  # Llama a la función process_files si el script se ejecuta directamente (no se importa como un módulo)
