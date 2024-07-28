import pandas as pd
from pathlib import Path

class ProcesadorDatosEmbarcaciones:
    def __init__(self, directorio):
        self.directorio = Path(directorio).resolve()

    def listar_archivos_nemos(self):
        # Listar archivos en el directorio especificado
        return [archivo.as_posix() for archivo in self.directorio.iterdir() if archivo.is_file()]

    def cargar_datos_nemos(self, lista_archivos):
        # Leer archivos y concatenar en un único DataFrame
        lista_dfs = []
        for archivo in lista_archivos:
            df = pd.read_csv(archivo, low_memory=False)
            lista_dfs.append(df)
        return pd.concat(lista_dfs, ignore_index=True)

    def renombrar_columnas_nemos(self, df):
        nuevo_nombre_columnas = {
                    'Unique_id': 'ID_Unico',
                    'Nave': 'Nombre_Embarcacion',
                    'Referencia': 'Ref_Posicion',
                    'Referenc_1': 'Ref_Auxiliar',
                    'Longitud': 'Longitud',
                    'Latitud': 'Latitud',
                    'Fecha y ho': 'Fecha_Hora',
                    'Fecha de l': 'Fecha_Log',
                    'Hora de la': 'Hora_Log',
                    'Marca de t': 'Tipo_Marca',
                    'Marca de_1': 'Subtipo_Marca',
                    'Guardar ma': 'Guardar_Marca',
                    'Rumbo': 'Rumbo',
                    'Rumbo prom': 'Rumbo_Promedio',
                    'Velocidad': 'Velocidad',
                    'Velocida_1': 'Velocidad_Promedio',
                    'Referenc_2': 'Ref_Secundaria',
                    'Dipoitivo': 'Dispositivo',
                    'Retrasar l': 'Retraso_Local',
                    'Dispositiv': 'Tipo_Dispositivo',
                    'Retraso Pr': 'Retraso_Promedio',
                    'Retraso re': 'Retraso_Reporte',
                    'ID zona de': 'ID_Zona',
                    'Dia': 'Dia',
                    'Mes': 'Mes',
                    'Anio': 'Anio',
                    'Viaje': 'ID_Viaje',
                    'Etapa': 'Etapa_Viaje',
                    'Inicio de viaje': 'Inicio_Viaje',
                    'Fin de viaje': 'Fin_Viaje',
                    'Unique_ID': 'ID_Unico_Alterno',
                    'Disposit_1': 'Detalle_Dispositivo',
                    'Inicio de Viaje': 'Inicio_Viaje_Detalle',
                    'Fin de Viaje': 'Fin_Viaje_Detalle'
        }
        columnas_existentes = df.columns
        columnas_a_renombrar = {key: value for key, value in nuevo_nombre_columnas.items() if key in columnas_existentes}
        return df.rename(columns=columnas_a_renombrar)

    def convertir_datetime(self, df):
        datetime_fields = ['Fecha_Hora', 'Fecha_Log', 'Hora_Log']
        formats = {
            'Fecha_Hora': '%d/%m/%Y %H:%M:%S',  # Ajusta estos formatos según tus datos
            'Fecha_Log': '%d/%m/%Y',
            'Hora_Log': '%H:%M:%S'
        }
        for field in datetime_fields:
            if field in df.columns:
                df[field] = pd.to_datetime(df[field], format=formats[field], errors='coerce')
        return df
    
    def eliminar_columnas_vacias(self, df):
        return df.dropna(axis=1, how='all')

    def limpiar_datos(self, df):
        # Eliminar filas duplicadas y manejar valores NaN adecuadamente
        df = df.drop_duplicates()
        df = df.fillna(value={"columna_con_NaNs": "valor_default"})  # Ejemplo específico
        return df
    
# Uso de la clase
procesador = ProcesadorDatosEmbarcaciones('NEMOS')
archivos = procesador.listar_archivos_nemos()
df = procesador.cargar_datos_nemos(archivos)
df_renombrado = procesador.renombrar_columnas_nemos(df)
df_limpio = procesador.limpiar_datos(df_renombrado)
df_final = procesador.convertir_datetime(df_limpio)
df_final = procesador.eliminar_columnas_vacias(df_final)

# Guardar el DataFrame final
df_final.to_csv('vms_flota_nemo.csv', encoding='utf-8', index=False)