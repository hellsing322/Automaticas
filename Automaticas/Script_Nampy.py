import os
import numpy as np
from Conecciones import create_ftp_connection
from io import BytesIO

def process_files() -> None:
    ftp = create_ftp_connection()

    folders = ['M001',]  # Tus nombres de carpetas conocidos

    all_data_list = []  # Lista para almacenar todos los datos

    for folder in folders:
        ftp.cwd(folder)  # Navega a la carpeta

        filenames = ftp.nlst()

        download_dir = r"C:\Users\JUANKAR\Pictures\Inamhi\Data"
        for filename in filenames:
            if filename.endswith(".rep"):
                r = BytesIO()
                ftp.retrbinary('RETR ' + filename, r.write)
                valoresEstacion = r.getvalue().decode('UTF-8').replace('\r', '')

                valoresEstacionFilas = valoresEstacion.split("\n")
                for valoresEstacionColumnas in valoresEstacionFilas:
                    if len(valoresEstacionColumnas.split(",")) > 1:
                        data = np.array(valoresEstacionColumnas.split(","), dtype=str)
                        all_data_list.append(data)

                os.remove(filename)

        ftp.cwd("..")  # Regresa al directorio principal antes de continuar con la próxima carpeta

        # Realizar cualquier procesamiento adicional aquí

    all_data = np.vstack(all_data_list)  # Convertir la lista en un array NumPy

    print(all_data)  # Imprimir el array completo

    ftp.quit()  # Cerrar la conexión FTP al finalizar

# Llamando a la función
process_files()
