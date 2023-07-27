import pandas as pd
from Conecciones import create_ftp_connection, create_postgres_connection
from niveles.nivel_0 import validate_data_level_0
from niveles.nivel_1 import validate_data_level_1
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
pd.set_option('display.max_rows', None)
def list_ftp_files():
    ftp = create_ftp_connection()
    # Obtener una lista de archivos en el directorio actual
    file_list = ftp.nlst()
    file_list = file_list[:2]
    print(file_list)
    return file_list

def read_files_from_ftp(folder_name):

    print(f"Thread s processing folder: {folder_name}")

    ftp = create_ftp_connection()
    ftp.cwd(folder_name)  # Cambiar al directorio de la carpeta
    print(f"Thread directorio")

    file_list = ftp.nlst()
    print(f"Thread s processing file: {file_list}")

    # Definir la función para leer y procesar un archivo específico
    def read_and_process_file(file_name):
        #print(f"Thread s processing folder: {folder_name}")

        with BytesIO() as f:
            ftp.retrbinary('RETR ' + file_name, f.write)  # Leer el contenido del archivo
            f.seek(0)
            df = pd.read_csv(f)
            df['Estacion'] = [folder_name] * len(df)
            df_cleaned = validate_data_level_0(df, file_name)
            df_cleaned = validate_data_level_1(df_cleaned,file_name)
            #df_cleaned = validate_data_level_1(df_cleaned, file_name) 
             # Limpiar los datos del DataFrame
            return file_name, df_cleaned  # Devolver tanto el file_name como el df limpiado como una tupla

    # Utilizar la función read_and_process_file con ThreadPoolExecutor en lugar del bucle for
    list(map(read_and_process_file, file_list))

    ftp.cwd('/')  # Volver al directorio raíz del servidor FTP



# Obtener la lista de nombres de archivos desde el directorio actual del servidor FTP
file_names_list = list_ftp_files()

# Procesar los DataFrames usando ThreadPoolExecutor y limpiar los datos en cada DataFrame
# num_threads = os.cpu_count() - 1
num_threads = 1
print("Número de hilos:", num_threads)
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Procesar los DataFrames usando hilos y limpiar los datos en cada DataFrame
    dataframes_with_names_list = list(executor.map(read_files_from_ftp, file_names_list))

# Separar los dataframes y la lista de archivos de la lista de tuplas
