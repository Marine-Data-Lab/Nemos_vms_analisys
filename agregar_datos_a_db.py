import pandas as pd
import sqlite3
from pathlib import Path

class ProcesadorDatosEmbarcaciones:
    def __init__(self, archivo_csv, db_path):
        self.archivo_csv = archivo_csv
        self.db_path = db_path

    def cargar_datos_csv(self):
        # Leer el archivo CSV
        df = pd.read_csv(self.archivo_csv, low_memory=False)
        return df

    def preprocesar_datos(self, df):
        # Renombrar columnas, convertir tipos de datos, etc.
        nuevo_nombre_columnas = {
            'Unique_id': 'ID_Unico',
            'Nave': 'Nombre_Embarcacion',
            # Continúa con el resto según tu definición
        }
        df.rename(columns=nuevo_nombre_columnas, inplace=True)
        
        # Convertir las columnas de fecha y hora
        campos_fecha = ['Fecha_Hora', 'Fecha_Log', 'Hora_Log']
        for campo in campos_fecha:
            if campo in df.columns:
                df[campo] = pd.to_datetime(df[campo], errors='coerce')

        # Limpieza de datos: eliminar filas duplicadas, manejar NaNs
        df.drop_duplicates(inplace=True)
        df.fillna(value={'Ref_Posicion': 'Desconocido'}, inplace=True)  # Ejemplo de manejo de NaN

        return df

    def cargar_datos_a_db(self, df):
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect(self.db_path)

        # Insertar los datos en la base de datos
        df.to_sql('datos_flota', conn, if_exists='append', index=False)

        # Cerrar la conexión
        conn.close()

def main():
    archivo_csv = 'vms_flota_nemo.csv'
    db_path = 'flota_nemo.db'

    procesador = ProcesadorDatosEmbarcaciones(archivo_csv, db_path)
    df = procesador.cargar_datos_csv()
    df_preprocesado = procesador.preprocesar_datos(df)
    procesador.cargar_datos_a_db(df_preprocesado)
    print("Datos cargados exitosamente en la base de datos.")

if __name__ == '__main__':
    main()
