import os
import numpy as np
import pandas as pd
from Conecciones import create_ftp_connection

pd.set_option('display.max_rows', None)  # Set pandas to display all rows

def process_files(folders):
    ftp = create_ftp_connection()

    def process_folder(folder):
        ftp.cwd(folder)  # Navega a la carpeta

        filenames = ftp.nlst()

        all_data = pd.concat([pd.read_csv(f) for f in filenames if f.endswith(".rep")])

        def is_numeric(x):
            return np.issubdtype(x.dtype, np.number)

        numeric_columns = all_data.select_dtypes(include=np.number).columns.tolist()

        # Filtering columns by name
        filtered_columns = list(filter(lambda x: not x.startswith('cdt') and x != 'fecha', numeric_columns))

        stats = all_data.loc[:, filtered_columns].agg(['count', 'mean', 'min', 'max']).T
        stats = stats.reset_index().rename(columns={'index': 'column'})
        stats['folder'] = folder
        print(stats)

        non_numeric_data = all_data.select_dtypes(exclude=np.number)
        # Filter out columns that start with 'cdt' or equal to 'fecha'
        non_numeric_filtered_columns = [col for col in non_numeric_data.columns if not col.startswith('cdt') and col != 'fecha']
        non_numeric_data = non_numeric_data[non_numeric_filtered_columns]
        
        if not non_numeric_data.empty:
            non_numeric_data = non_numeric_data.dropna(how='all')
            non_numeric_data = non_numeric_data.melt(var_name='column', value_name='non-numeric value')
            non_numeric_data['folder'] = folder
            print(non_numeric_data)

        ftp.cwd("..")  # Regresa al directorio principal antes de continuar con la próxima carpeta

    # Process each folder
    list(map(process_folder, folders))

# Llamando a la función
process_files(['M001',])  # Tus nombres de carpetas conocidos
