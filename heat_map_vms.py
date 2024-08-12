import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd

import pandas as pd
import glob
import os

# Especifica la ruta de la carpeta que contiene los archivos CSV
carpeta_csv = 'archivos_filtrados'  # Cambia esta ruta a la de tu carpeta

# Usa glob para encontrar todos los archivos CSV en la carpeta
archivos_csv = glob.glob(os.path.join(carpeta_csv, '*.csv'))

# Crea una lista para almacenar cada DataFrame individual
dataframes = []

# Diccionario de renombre de columnas
columnas_renombradas = {
    'Nombre': 'Nombre_Embarcacion',
    'Puerto_Base': 'Puerto Base',
    'Razón Social': 'Permisionario o concesionario',
    'Pemisionario o Concesionario': 'Permisionario o concesionario'
}

# Itera sobre la lista de archivos CSV y lee cada uno en un DataFrame
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    
    # Renombrar las columnas según el diccionario
    df.rename(columns=columnas_renombradas, inplace=True)
    
    # Eliminar la columna 'Unnamed: 9' si existe
    if 'Unnamed: 9' in df.columns:
        df.drop(columns=['Unnamed: 9'], inplace=True)
    
    dataframes.append(df)

# Concatena todos los DataFrames en uno solo
df_concatenado = pd.concat(dataframes, ignore_index=True)

# Guarda el DataFrame concatenado en un nuevo archivo CSV
df_concatenado.to_csv('vms_concatenado.csv', index=False)  # Cambia esta ruta y nombre de archivo según tus necesidades

print(f'Se han unido {len(archivos_csv)} archivos CSV en un único DataFrame y se ha guardado como csv_concatenado.csv')

##################### PASAR A OTRO SCRIPT  ###################

# Cargar los datos desde el archivo CSV
data_vms = pd.read_csv('vms_concatenado.csv',low_memory=False)

# Asegurarse de que la columna 'Fecha' es de tipo datetime
data_vms['Fecha'] = pd.to_datetime(data_vms['Fecha'],errors='coerce')
lista_emb= pd.read_csv('lista_emb.csv')
data_vms = df_concatenado[df_concatenado['Nombre_Embarcacion'].isin(lista_emb)]
# Filtrar los datos por año
data_year = data_vms.loc[data_vms['Fecha'].dt.year == 2018].copy()

data_vms.to_csv('vms_GM_2018.csv')

##################### Otro script ###################
# Cargar los datos
vms_2018 = pd.read_csv('vms_GM_2018.csv')
vertices = pd.read_csv('vms_vertices_GM.csv')

# Convertir los datos a GeoDataFrame
vms_2018['geometry'] = gpd.points_from_xy(vms_2018.Longitud, vms_2018.Latitud)


# Convert 'Fecha' to datetime
vms_2018['Fecha'] = pd.to_datetime(vms_2018['Fecha'])


# Determinar los límites del mapa
minx, miny = vertices[['Longitud', 'Latitud']].min()
maxx, maxy = vertices[['Longitud', 'Latitud']].max()

# Crear la figura
fig, axes = plt.subplots(1, 1, figsize=(18, 12))

# Función para crear un mapa de calor con mapa base
def heatmap(ax, x, y, title, vmin=0, vmax=500):
    hb = ax.hexbin(x, y, gridsize=40, cmap='cividis', mincnt=5, vmin=vmin, vmax=vmax)
    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom=6, crs='EPSG:4326')
    ax.set_title(title)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    cb = fig.colorbar(hb, ax=ax, orientation='vertical')
    cb.set_label('Counts')

# Plotear los datos de 2018
heatmap(axes[0, 0], vms_2018.Longitud, vms_2018.Latitud, '2018')

# Mostrar la figura
plt.tight_layout()
plt.show()